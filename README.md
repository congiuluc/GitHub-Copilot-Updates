# 🚀 GitHub Copilot Updates Generator

Welcome! This tool helps you automatically generate using **GitHub Copilot Agent** professional PowerPoint presentations summarizing the latest GitHub Copilot updates. 

Stop copy-pasting release notes. Let your AI agent do the work for you.

## ✨ What This Tool Does

1.  **Retrieves Updates**: Scrapes the official GitHub Copilot changelog for a specific time range.
2.  **Analyzes Content**: Summarizes key features and generates speaker notes in both English and Italian.
3.  **Creates PowerPoint**: Generates a formatted `.pptx` presentation with title slides, focal points, and speaker notes included.

---

## 🏎️ Quick Start (The Easy Way)

**Prerequisites:**
- Visual Studio Code with GitHub Copilot Chat.
- This workspace open in VS Code.

**How to use:**
1.  Open **GitHub Copilot Chat** in the sidebar.
2.  Copy one of the [Prompt Samples](#-prompt-samples) below.
3.  Paste it into the chat and hit Enter.
4.  Find your presentation in the `pptx/` folder!

---

## 💬 Prompt Samples

Simply copy and paste these into Copilot Chat:

### 📅 This Month's Updates
```text
Get all GitHub Copilot updates from January 2026 and generate a PowerPoint presentation.
```
> **Creates:** A slide deck for the current month's features.  
> **Good for:** Monthly team syncs.

### 📊 Quarterly Review
```text
Get all GitHub Copilot updates from October 2025 to December 2025 and create a comprehensive PowerPoint presentation.
```
> **Creates:** A comprehensive deck covering multiple months.  
> **Good for:** QBRs and strategic planning.

### ⏱️ Weekly Briefing
```text
Get GitHub Copilot updates from January 13 to January 19, 2026 for this week's team briefing.
```
> **Creates:** A short, focused deck for a specific week.  
> **Good for:** Weekly standups.

### 📚 Full Archive
```text
Create a comprehensive archive of all GitHub Copilot updates from January 2025 through January 2026.
```
> **Creates:** A massive archive deck spanning a year.  
> **Good for:** Onboarding and historical reference.

---

## 🛠️ Technical Setup (Only if you run scripts manually)

If you prefer to run the Python scripts directly via terminal instead of using the Chat Agent:

1.  **Install Python**: Ensure Python 3.10+ is installed.
2.  **Install Library**:
    ```bash
    pip install python-pptx
    ```
3.  **Run Script**:
    ```bash
    # Example: Generate PPT from existing markdown files
    python scripts/markdown_to_ppt.py --from 2026-01-01
    ```

**(Optional) Pandoc Support**:
If you plan to use `markdown_to_pandoc.py` for PDF/HTML generation, install Pandoc:
- Windows: `choco install pandoc`
- macOS: `brew install pandoc`
- Linux: `sudo apt-get install pandoc`

---

## 📄 License

**MIT License**

Copyright (c) 2026 GitHub Copilot Updates Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
