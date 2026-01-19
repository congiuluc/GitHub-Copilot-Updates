"""
Convert markdown files to Pandoc slide deck format.
Creates a presentation with cover slides (image background + white title) and content slides.

Usage:
    python markdown_to_pandoc.py                           # Process all markdown files in updates/YYYY/MM/
    python markdown_to_pandoc.py --from 2025-09-01         # From specific date onwards
    python markdown_to_pandoc.py --from 2025-09-01 --to 2025-09-30  # Date range
    python markdown_to_pandoc.py --output presentation.md   # Specify output filename
    python markdown_to_pandoc.py --format revealjs          # Specify Pandoc output format (default: beamer)

Pandoc can then convert this to various formats:
    pandoc presentation.md -t beamer -o presentation.pdf
    pandoc presentation.md -t revealjs -o presentation.html
    pandoc presentation.md -t pptx -o presentation.pptx
"""

import os
import re
import argparse
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError
import time

def fetch_og_image_from_url(url):
    """
    Fetch the og:image meta tag from a given URL with retry logic.
    
    Args:
        url: URL to fetch og:image from
    
    Returns:
        og:image URL if found, None otherwise
    """
    max_retries = 3
    delays = [1, 2, 4]  # Retry delays in seconds: 1s, 2s, 4s
    
    for attempt in range(max_retries):
        try:
            req = Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            
            with urlopen(req, timeout=5) as response:
                html_content = response.read().decode('utf-8', errors='ignore')
                
                og_image_match = re.search(
                    r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']+)["\']|'
                    r'<meta\s+content=["\']([^"\']+)["\']\s+property=["\']og:image["\']',
                    html_content,
                    re.IGNORECASE
                )
                
                if og_image_match:
                    return og_image_match.group(1) or og_image_match.group(2)
        
        except (URLError, Exception) as e:
            if attempt < max_retries - 1:
                delay = delays[attempt]
                # Silently retry without printing to avoid cluttering output
                time.sleep(delay)
                continue
            else:
                # Final attempt failed, proceed without image
                pass
    
    return None

def parse_markdown_file(file_path):
    """
    Parse markdown file and extract:
    - Article title (from # Article Title)
    - Article date (from ## Article Date)
    - Article link (from ## Article Url)
    - Article image (from ## Article Image or fetched from og:image)
    - Focal points (from ## Article Content with bullet points)
    - Speaker notes (from ### Speaker Notes)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title_match = re.search(r'^# (.+?)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else "Untitled"
    
    date_match = re.search(r'## Article Date\n(.+?)$', content, re.MULTILINE)
    article_date = date_match.group(1).strip() if date_match else ""
    
    link_match = re.search(r'## Article Url\n(.+?)$', content, re.MULTILINE)
    article_link = link_match.group(1).strip() if link_match else ""
    
    image_match = re.search(r'## Article Image\n(.+?)$', content, re.MULTILINE)
    article_image = image_match.group(1).strip() if image_match else ""
    
    # Always fetch from og:image meta tag
    if article_link:
        fetched_image = fetch_og_image_from_url(article_link)
        if fetched_image:
            article_image = fetched_image
    
    focal_section = re.search(
        r'## Article Content\n((?:.|\n)+?)(?:^###|\Z)',
        content,
        re.MULTILINE
    )
    focal_points = []
    if focal_section:
        points_text = focal_section.group(1)
        for line in points_text.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            if line.startswith('• ') or line.startswith('- '):
                point = line[2:].strip()
                focal_points.append(point)
            elif line.startswith('**') and '**' in line[2:]:
                focal_points.append(line)
    
    speaker_section = re.search(
        r'### Speaker Notes\n((?:.|\n)+?)(?:^##[^#]|^##$|\Z)',
        content,
        re.MULTILINE
    )
    speaker_notes = ""
    if speaker_section:
        speaker_notes = speaker_section.group(1).strip()
    
    return {
        'title': title,
        'date': article_date,
        'link': article_link,
        'image': article_image,
        'focal_points': focal_points,
        'speaker_notes': speaker_notes
    }

def create_cover_slide_markdown(title, image_url, date=""):
    """
    Create a cover slide with image as background and white title.
    Uses Pandoc's native slide format.
    
    Args:
        title: Article title
        image_url: URL to the article image
        date: Article date
    
    Returns:
        Markdown string for cover slide
    """
    markdown = ""
    
    # Add cover slide with background image
    if image_url and image_url != "https://github.blog/changelog/":
        markdown += f"# {title}\n\n"
        markdown += f"![](./media/{os.path.basename(image_url)}){{.background}}\n\n"
    else:
        markdown += f"# {title}\n\n"
    
    markdown += "---\n\n"
    
    return markdown

def create_content_slide_markdown(title, focal_points, date, speaker_notes, link=""):
    """
    Create a content slide with title, bullet points, date footer and speaker notes.
    
    Args:
        title: Slide title
        focal_points: List of focal points
        date: Date to display in bottom right
        speaker_notes: Speaker notes text
        link: Article link
    
    Returns:
        Markdown string for content slide
    """
    markdown = ""
    
    # Add title
    markdown += f"## {title}\n\n"
    
    # Add focal points as bullets
    for point in focal_points:
        markdown += f"- {point}\n"
    
    # Add speaker notes section using Pandoc notes format
    if speaker_notes or link:
        markdown += "\n::: notes\n\n"
        if link:
            markdown += f"**Article Link**: {link}\n\n"
        
        # Parse and format speaker notes with all content
        markdown += speaker_notes
        markdown += "\n\n:::\n"
    
    # Add date footer (Pandoc doesn't support footer metadata in standard way,
    # so we add it as a note or special format)
    markdown += f"\n<!-- Date: {date} -->\n"
    
    markdown += "\n---\n\n"
    
    return markdown

def filter_files_by_date(files, date_from=None, date_to=None):
    """Filter markdown files by date range."""
    filtered = []
    
    for file_path in files:
        match = re.match(r'(\d{4}-\d{2}-\d{2})', file_path.name)
        if not match:
            continue
        
        file_date = match.group(1)
        
        try:
            file_datetime = datetime.strptime(file_date, '%Y-%m-%d')
            
            if date_from:
                from_datetime = datetime.strptime(date_from, '%Y-%m-%d')
                if file_datetime < from_datetime:
                    continue
            
            if date_to:
                to_datetime = datetime.strptime(date_to, '%Y-%m-%d')
                if file_datetime > to_datetime:
                    continue
            
            filtered.append(file_path)
        except ValueError:
            continue
    
    return filtered

def main():
    """Process markdown files and generate Pandoc-compatible slide deck."""
    
    parser = argparse.ArgumentParser(
        description='Convert markdown files to Pandoc slide deck format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python markdown_to_pandoc.py                                   # Create presentation.md
  python markdown_to_pandoc.py --from 2025-09-01                # From date onwards
  python markdown_to_pandoc.py --from 2025-09-01 --to 2025-09-30 # Date range
  python markdown_to_pandoc.py --output slides.md               # Specify output filename
  python markdown_to_pandoc.py --format revealjs                # Specify Pandoc format

Pandoc conversion examples:
  pandoc presentation.md -t beamer -o presentation.pdf
  pandoc presentation.md -t revealjs -o presentation.html
  pandoc presentation.md -t pptx -o presentation.pptx
        """
    )
    
    parser.add_argument(
        '--from',
        dest='date_from',
        type=str,
        help='Start date (YYYY-MM-DD) to filter markdown files'
    )
    parser.add_argument(
        '--to',
        dest='date_to',
        type=str,
        help='End date (YYYY-MM-DD) to filter markdown files'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='presentation.md',
        help='Output markdown filename (default: presentation.md)'
    )
    parser.add_argument(
        '--format',
        type=str,
        default='beamer',
        choices=['beamer', 'revealjs', 'slidy', 'slideous'],
        help='Pandoc output format (default: beamer)'
    )
    
    args = parser.parse_args()
    
    current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    updates_dir = current_dir / 'updates'
    
    if not updates_dir.exists():
        print(f"✗ Updates directory not found: {updates_dir}")
        return
    
    # Recursively search for markdown files in YYYY/MM/ subdirectories
    markdown_files = []
    for year_dir in sorted(updates_dir.glob('[0-9][0-9][0-9][0-9]')):
        if year_dir.is_dir():
            for month_dir in sorted(year_dir.glob('[0-9][0-9]')):
                if month_dir.is_dir():
                    markdown_files.extend(month_dir.glob('*.md'))
    
    # Sort all files by filename
    markdown_files = sorted(markdown_files)
    
    if not markdown_files:
        print("✗ No markdown files found in updates directory")
        return
    
    # Filter by date if specified
    if args.date_from or args.date_to:
        markdown_files = filter_files_by_date(markdown_files, args.date_from, args.date_to)
        
        if args.date_from and args.date_to:
            print(f"📅 Filtering files from {args.date_from} to {args.date_to}")
        elif args.date_from:
            print(f"📅 Filtering files from {args.date_from} onwards")
        elif args.date_to:
            print(f"📅 Filtering files up to {args.date_to}")
    
    if not markdown_files:
        print("✗ No markdown files found in the specified date range")
        return
    
    # Generate unique filename based on date filters if using default output name
    if args.output == 'presentation.md' and (args.date_from or args.date_to):
        if args.date_from and args.date_to:
            output_md = f"presentation_{args.date_from}_to_{args.date_to}.md"
        elif args.date_from:
            output_md = f"presentation_from_{args.date_from}.md"
        else:
            output_md = f"presentation_to_{args.date_to}.md"
    else:
        output_md = args.output
    
    # Start building the presentation
    pandoc_content = ""
    
    # Add YAML front matter for metadata
    pandoc_content += "---\n"
    pandoc_content += "title: GitHub Updates Presentation\n"
    pandoc_content += f"date: {datetime.now().strftime('%Y-%m-%d')}\n"
    pandoc_content += "author: Generated Presentation\n"
    pandoc_content += f"theme: default\n"
    if args.format == 'beamer':
        pandoc_content += "colortheme: default\n"
    pandoc_content += "---\n\n"
    
    processed_count = 0
    for md_file in markdown_files:
        try:
            # Parse markdown file
            data = parse_markdown_file(str(md_file))
            
            # Add cover slide with image background and white title
            pandoc_content += create_cover_slide_markdown(
                data['title'],
                data['image'],
                data['date']
            )
            
            # Add content slide
            pandoc_content += create_content_slide_markdown(
                data['title'],
                data['focal_points'],
                data['date'],
                data['speaker_notes'],
                data['link']
            )
            
            print(f"✓ Added slides from: {md_file.name}")
            processed_count += 1
        except Exception as e:
            print(f"✗ Error processing {md_file.name}: {e}")
    
    # Save the presentation
    if processed_count > 0:
        with open(output_md, 'w', encoding='utf-8') as f:
            f.write(pandoc_content)
        print(f"\n✓ Saved Pandoc presentation: {output_md}")
        
        # Generate output filename without extension
        output_base = output_md.replace('.md', '')
        pptx_output = f"{output_base}.pptx"
        
        # Ask user if they want to convert to PPTX
        print(f"\n❓ Would you like to convert to PowerPoint (widescreen)?")
        print(f"   Command: pandoc {output_md} -t pptx -o {pptx_output}")
        
        user_input = input("\nProceed with PPTX conversion? (y/n): ").strip().lower()
        
        if user_input == 'y' or user_input == 'yes':
            try:
                import subprocess
                result = subprocess.run(
                    ['pandoc', output_md, '-t', 'pptx', '-o', pptx_output],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    print(f"\n✓ Successfully created: {pptx_output}")
                else:
                    # Check if error is about missing media files
                    if "not found in resource path" in result.stderr or "file not found" in result.stderr.lower():
                        print(f"\n⚠ Warning: Some media files were not found during conversion")
                        print(f"   This is expected - images will be referenced as URLs in the presentation")
                        print(f"   The presentation was created, but without embedded images")
                        
                        # Try to create PPTX anyway by removing image references
                        print(f"\n   Attempting to create presentation without image references...")
                        
                        # Read the markdown and remove image syntax
                        with open(output_md, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Remove background image references
                        content_no_images = re.sub(r'!\[\]\(\.\/media\/[^)]+\)\{\.background\}\n+', '', content)
                        
                        # Temporarily save modified version
                        temp_md = output_md.replace('.md', '_no_images.md')
                        with open(temp_md, 'w', encoding='utf-8') as f:
                            f.write(content_no_images)
                        
                        # Try conversion again without images
                        result_retry = subprocess.run(
                            ['pandoc', temp_md, '-t', 'pptx', '-o', pptx_output],
                            capture_output=True,
                            text=True
                        )
                        
                        # Clean up temp file
                        try:
                            os.remove(temp_md)
                        except:
                            pass
                        
                        if result_retry.returncode == 0:
                            print(f"✓ Successfully created: {pptx_output} (without background images)")
                        else:
                            print(f"✗ Pandoc conversion failed: {result_retry.stderr}")
                            print(f"   Make sure Pandoc is installed: https://pandoc.org/installing.html")
                    else:
                        print(f"\n✗ Pandoc conversion failed: {result.stderr}")
                        print(f"   Make sure Pandoc is installed: https://pandoc.org/installing.html")
            except FileNotFoundError:
                print(f"\n✗ Pandoc not found. Please install it first:")
                print(f"   Windows: choco install pandoc")
                print(f"   macOS: brew install pandoc")
                print(f"   Linux: sudo apt-get install pandoc")
                print(f"\n   Or manually run: pandoc {output_md} -t pptx -o {pptx_output}")
        else:
            print(f"\n📋 Other conversion options:")
            print(f"   pandoc {output_md} -t beamer -o {output_base}.pdf")
            print(f"   pandoc {output_md} -t revealjs -o {output_base}.html -s")
            print(f"   pandoc {output_md} -t slidy -o {output_base}.html -s")
    else:
        print(f"\n✗ No slides were created")
    
    print(f"✓ Successfully processed {processed_count} markdown file(s)")

if __name__ == '__main__':
    main()
