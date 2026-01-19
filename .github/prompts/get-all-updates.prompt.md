---
description: GitHub Copilot Updates Documentation Generator - Retrieves changelog articles for a specified month/year and generates structured markdown documentation with multilingual speaker notes for presentations.
---

## Workflow Overview

This workflow provides a systematic three-stage process for generating GitHub Copilot changelog documentation:

1. **Input Collection** - Request month and year parameters
2. **Planning Stage** - Retrieve articles and generate a structured execution plan
3. **Generation Stage** - Create markdown files with speaker notes in multiple languages

---

## Stage 1: Input Collection

**Request the following from the user:**
- **Month**: Integer value from 1-12 (January = 1, December = 12)
- **Year**: Full year value (e.g., 2025)

Do not proceed to Stage 2 until both parameters are provided.

---

## Stage 2: Planning & Validation

**Retrieve changelog content - COMPREHENSIVE MULTI-STEP APPROACH (GET ALL ARTICLES BY URL):**

**Step 1: Complete month retrieval (ALL articles, NO label filters):**
   ```
   https://github.blog/changelog/{year}/{month:02d}/
   ```
   - Replace `{year}` with the provided year (e.g., 2025)
   - Replace `{month:02d}` with zero-padded month number (e.g., 01-12)
   - Retrieve the full changelog page for the entire month WITHOUT any label filters
   - This captures ALL articles including those with single or multiple labels
   - Document article count from complete month view

**Step 2: Pagination verification:**
   - Check if the changelog page has multiple pages or infinite scroll
   - If pagination exists, retrieve all pages for the specified month
   - If infinite scroll, scroll to bottom to ensure all articles load
   - Document total article count from full month view

**Step 3: Multi-label article validation:**
   - Pay special attention to articles with multiple labels/categories
   - Articles may have tags like: COPILOT, CLIENT APPS, ACCOUNT MANAGEMENT, SECURITY, PLATFORM, AUTHENTICATION, etc.
   - **IMPORTANT**: Do NOT skip articles with multiple labels - include them in final list
   - Verify each article's URL is captured even if it appears under multiple categories
   - Document articles with multiple labels separately in retrieval notes

**Step 4: GitHub Blog archive verification:**
   - Visit `https://github.blog/changelog/` to access archive navigation
   - Cross-verify the article titles and count for the specified month match Step 1-2
   - If discrepancies found, retrieve directly from archive month page

**Extract metadata for ALL articles in the specified month:**
- Article title (complete, exact match from webpage)
- Publication date (yyyy-MM-dd format)
- Article URL (complete URL path)
- Article image URL (from `og:image` meta tag in article header)
- Article label/category (COPILOT, CLIENT APPS, ACCOUNT MANAGEMENT, SECURITY, PLATFORM, AUTHENTICATION, etc.)

**Validation requirements - CRITICAL:**
- Count total articles displayed on the webpage(s) after removing duplicates
- Verify complete coverage by exhaustively checking all sections, pagination, and labels
- Document article count at each retrieval step (Copilot-only, All categories, After pagination)
- If article count differs between steps, retrieve unfiltered month page to establish definitive total
- Create a verification checklist with ALL visible article titles organized by retrieval step
- **Final validation**: Compare final article count with GitHub Blog changelog page display - they MUST match
- Confirm no articles from the specified month are missing from your compiled list

**Batch organization:**
- Group articles into processing batches of **maximum 5 items each**
- Assign batch numbers (Batch 1, Batch 2, etc.)
- Generate proposed filenames using format: `yyyy-MM-dd-article-title-slug`
  - Use lowercase letters
  - Replace spaces with hyphens
  - Remove special characters (retain hyphens only)

**Plan document:**
- Determine date range:
  - Identify earliest and latest publication dates
  - For single date, use: `plan-{date}.md`
  - For date range, use: `plan-{date_from}-to-{date_to}.md`
- Save location: `updates/{year}/{month}/`
- Plan header MUST include:
  - Total article count (verified against GitHub changelog webpage)
  - Month and year being processed
  - Date range of articles
  - Retrieval summary (total articles found using unfiltered URL retrieval)
- Format as markdown table with columns:

  | Batch | Filename | Date | Title | URL | Image URL | Label |

**Pre-presentation verification - COMPLETENESS CHECK:**
- [ ] **Total article count VERIFIED** - Count matches GitHub Blog changelog webpage display for the month
- [ ] Date range (earliest to latest) is clearly documented
- [ ] All article titles from the month are listed with exact matches to source
- [ ] Article count from final retrieval = articles in compiled list (NO MISSING ARTICLES)
- [ ] Retrieval methodology: Used unfiltered month URL to capture ALL articles regardless of single or multiple labels
- [ ] Articles with multiple labels are included (NOT skipped)
- [ ] Pagination fully processed or confirmed as none
- [ ] No duplicate entries (by URL, same article with multiple labels counted once)
- [ ] All URLs are complete and valid (include full domain path)
- [ ] All image URLs are complete and valid
- [ ] All articles are assigned all applicable labels from source
- [ ] Articles are batched with 5 or fewer items per batch
- [ ] Total batch count matches total articles

**Critical cross-check before presenting plan:**
1. Retrieve the GitHub Blog changelog page one final time
2. Count all visible articles for the specified month
3. Verify your compiled list matches this final count exactly
4. If mismatch exists, re-retrieve any missing content before presenting plan
5. Present plan only when counts match definitively

---

## Stage 3: Markdown Generation

Proceed only after receiving explicit user confirmation of the plan.

**Create one markdown file per article:**
- Location: `updates/{year}/{month}/{filename}.md`
- Filename format: `yyyy-MM-dd-article-title-slug.md`

**Markdown structure (exact format required):**

```markdown
# [Article Title]

## Article Date
yyyy-MM-dd

## Article Url
[Full URL to article]

## Article Image
[Full URL to og:image from article metadata]

## Article Content

- **[Key Point Title]**: [Brief 1-2 sentence description]
- **[Key Point Title]**: [Brief 1-2 sentence description]
- **[Key Point Title]**: [Brief 1-2 sentence description]
(up to 6 bullet points)

## Speaker Notes
### **Article Date**: yyyy-MM-dd - **Article Url**: [URL]
### **Article Image**: [Image URL]

### **Speaker Notes (Italian)**: 
**Apertura**: [Comprehensive opening of 2-3 sentences introducing the topic, explaining what problem it solves or opportunity it creates, and why it matters to developers and teams]
**Punti Principali**: 
- [Main point 1: 2-3 sentences explaining the feature, how it works, what changed, and practical benefits with real-world context]
- [Main point 2: 2-3 sentences explaining the feature, how it works, what changed, and practical benefits with real-world context]
- [Main point 3: 2-3 sentences explaining the feature, how it works, what changed, and practical benefits with real-world context]
(up to 6 main points, each substantive and discursive)

**Punti Focali Chiave**: 
- **[Focal Point 1]**: [Business impact or user benefit - 2-3 sentences]
- **[Focal Point 2]**: [Technical advantage or workflow improvement - 2-3 sentences]
- **[Focal Point 3]**: [Real-world application or use case - 2-3 sentences]
(2-4 focal points total, each substantive and integrated into speaker narrative)

**Implicazioni**: [Thorough description of broader impact on workflows, productivity, and organizational outcomes - 3-4 sentences]
**Conclusione**: [Summary of key takeaways and actionable guidance for teams - 2-3 sentences]

### **Speaker Notes (English)**: 
**Opening**: [Comprehensive opening of 2-3 sentences introducing the topic, explaining what problem it solves or opportunity it creates, and why it matters to developers and teams]
**Main Points**: 
- [Main point 1: 2-3 sentences explaining the feature, how it works, what changed, and practical benefits with real-world context]
- [Main point 2: 2-3 sentences explaining the feature, how it works, what changed, and practical benefits with real-world context]
- [Main point 3: 2-3 sentences explaining the feature, how it works, what changed, and practical benefits with real-world context]
(up to 6 main points, each substantive and discursive)

**Key Focal Points**: 
- **[Focal Point 1]**: [Business impact or user benefit - 2-3 sentences]
- **[Focal Point 2]**: [Technical advantage or workflow improvement - 2-3 sentences]
- **[Focal Point 3]**: [Real-world application or use case - 2-3 sentences]
(2-4 focal points total, each substantive and integrated into speaker narrative)

**Implications**: [Thorough description of broader impact on workflows, productivity, and organizational outcomes - 3-4 sentences]
**Conclusion**: [Summary of key takeaways and actionable guidance on how teams should adopt or leverage this capability - 2-3 sentences]
```

**Article Content guidelines:**
- Extract 4-6 key points from the article
- Focus on technical substance: features, improvements, and capabilities
- Keep descriptions concise and developer-focused
- Avoid marketing language; prioritize technical accuracy

**Speaker Notes guidelines:**
- Provide notes structured in both languages
- **Opening**: Provide a comprehensive introduction that explains the article content, its context, and why it matters (2-3 sentences). Include what problem it solves or what opportunity it addresses for developers and teams.
- **Main Points**: Detailed bullet list with 3-6 points, each being discursive and substantive:
  - Each point should be 2-3 sentences, not just one sentence
  - Focus on technical details and practical benefits with concrete explanations
  - Explain what changed, how it works, and why it matters to daily development workflows
  - Include context about the feature, its capabilities, and real-world applications
  - Connect each point to developer productivity, team efficiency, or business outcomes
- **Key Focal Points**: Moved to Speaker Notes from Article Content. Include 2-4 focal points, each with 2-3 substantive sentences:
  - Explain why this matters to developers
  - Address practical questions: "How does this improve development workflows?"
  - Include concrete use cases and technical implications
  - Use clear, straightforward language suitable for engineering teams
- **Implications**: Thoroughly describe the broader impact on development workflows, team productivity, and organizational benefits (3-4 sentences)
- **Conclusion**: Summarize key takeaways and provide actionable guidance on how teams should adopt or leverage this capability (2-3 sentences)
- Total per language: 200-250 words (expanded from 120-150 to allow for discursive content)
- Use direct, technical language; avoid jargon where possible
- Include specific details, examples, and use cases when applicable
- Maintain professional tone that respects developer expertise
- Write as if explaining to a knowledgeable technical audience who wants to understand practical implications

**Processing approach:**
- Generate files in batches of **up to 5 per batch**
- Before creating each file, check if it already exists
- If a file exists, request user confirmation:
  - "File `{filename}.md` already exists. Replace? (yes/no)"
  - Skip if user answers "no"
  - Overwrite if user answers "yes"
- Create all files in a batch simultaneously
- Confirm batch completion before proceeding to the next batch

---

## Quality Assurance Checklist

Before delivery - COMPLETENESS VERIFICATION:
- [ ] **Final article count VERIFIED** - Matches GitHub Blog changelog webpage for specified month
- [ ] No articles from the month are missing from the final delivery
- [ ] Article count: [X] files created = [X] articles on GitHub changelog webpage
- [ ] Complete cross-verification against source performed before file creation
- [ ] Plan header clearly displays total article count with verification summary
- [ ] All articles from the month are included, regardless of category or label count
- [ ] Articles with multiple labels are included in final delivery (NOT excluded)
- [ ] Retrieval methodology documented: Used unfiltered month URL to capture all articles
- [ ] Filenames follow `yyyy-MM-dd-title` format (lowercase, hyphenated)
- [ ] All metadata is complete and accurate (date, URL, image, label)
- [ ] All markdown files contain required sections in correct order
- [ ] **Markdown format validation for each file:**
  - [ ] H1 title: `# [Article Title]`
  - [ ] H2 sections: `## Article Date`, `## Article Url`, `## Article Image`, `## Article Content`, `## Speaker Notes`
  - [ ] H3 subsections: `### **Article Date**: ...`, `### **Speaker Notes (Italian):`, `### **Speaker Notes (English):**`
  - [ ] Bold sections: `**Apertura:**`, `**Punti Principali:**`, `**Punti Focali Chiave:**`, `**Implicazioni:**`, `**Conclusione:**`
  - [ ] English sections: `**Opening:**`, `**Main Points:**`, `**Key Focal Points:**`, `**Implications:**`, `**Conclusion:**`
  - [ ] Bullet points properly formatted with `-` or `*`
  - [ ] No markdown syntax errors or malformed sections
- [ ] Article Content includes 4-6 clear, technical bullet points
- [ ] Speaker Notes include Key Focal Points moved from Article Content section
- [ ] Key Focal Points in Speaker Notes (both languages) include 2-3 substantive sentences each
- [ ] Speaker Notes are structured with Opening, Main Points, Key Focal Points, Implications, Conclusion (both languages)
- [ ] Speaker Notes available in both Italian and English (200-250 words each)
- [ ] Speaker Notes include specific details, metrics, or examples
- [ ] Language is professional and appropriate for technical audiences
- [ ] All files saved to `updates/{year}/{month}/`
- [ ] Plan document saved with correct naming convention
- [ ] Batch organization follows 5-items-per-batch standard
- [ ] No duplicate entries in final delivery
- [ ] Final file count in updates/{year}/{month}/ directory matches article count in plan

