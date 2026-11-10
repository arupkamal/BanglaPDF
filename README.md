# Bengali Markdown to PDF Generator

A Python script that turns a **Bengali story written in Markdown** into a **PDF**. The text is laid out in a **centred 5-inch column** and paragraphs are **fully justified**. Bengali conjuncts (যুক্তাক্ষর) are drawn correctly using the **Kalpurush** font.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Features](#2-features)
3. [Requirements](#3-requirements)
4. [Installation](#4-installation)
5. [Font Setup](#5-font-setup)
6. [Quick Start](#6-quick-start)
7. [Configuration Reference](#7-configuration-reference)
8. [How It Works](#8-how-it-works)
9. [Code Structure](#9-code-structure)
10. [Supported Markdown](#10-supported-markdown)
11. [Customisation Recipes](#11-customisation-recipes)
12. [Troubleshooting](#12-troubleshooting)
13. [Known Limitations](#13-known-limitations)
14. [FAQ](#14-faq)

---

## 1. Overview

Bengali needs **complex text shaping**. Letters combine into conjuncts such as **জ্ঞ**, **ন্ত্র** and **প্র**, and vowel signs change position around letters. Many PDF libraries don't do this, so the text comes out broken.

This script solves the problem with:

| Component | Role |
|---|---|
| **fpdf2** | Creates the PDF and lays out the text |
| **uharfbuzz** | Shapes the text so Bengali conjuncts render correctly |
| **markdown** | Converts Markdown into HTML |
| **Kalpurush font** | A Unicode Bengali TrueType font |

The script is a simple procedural program with no classes. It runs in **Jupyter Notebook** and as a normal **`.py` script** on **Windows**.

---

## 2. Features

- ✅ Correct Bengali conjuncts and vowel signs
- ✅ Fixed-width column (5 inches by default), centred on the page
- ✅ Fully justified paragraphs
- ✅ Markdown support: headings, bold, italic, lists, quotes, horizontal lines
- ✅ Long text continues onto new pages automatically
- ✅ Finds the font automatically in the script folder and in the Windows font folders
- ✅ Works in Jupyter (no `__file__` error)
- ✅ Built-in sample text for testing
- ✅ All settings in one block at the top of the script
- ✅ Opens the finished PDF automatically (optional)

---

## 3. Requirements

| Requirement | Version / Notes |
|---|---|
| Operating system | Windows 10 / 11 |
| Python | 3.8 or newer recommended |
| `fpdf2` | Recent version (2.7.5 or newer for text shaping; newer versions handle justified, shaped text better) |
| `uharfbuzz` | Any recent version |
| `markdown` | Any recent version |
| Font | `kalpurush.ttf`, the **Unicode** version |

> ⚠️ **Important:** install `fpdf2`, **not** the old `fpdf` package. Both use `from fpdf import FPDF`, and having both installed causes conflicts. If you're not sure, run `pip uninstall fpdf` first.

---

## 4. Installation

### Option A: Command Prompt

```bash
pip install --upgrade fpdf2 uharfbuzz markdown
```

### Option B: Jupyter Notebook

```python
%pip install --upgrade fpdf2 uharfbuzz markdown
```

Then restart the kernel (**Kernel → Restart**) so the new packages load.

### Check the installation

```python
import fpdf, uharfbuzz, markdown
print("fpdf2   :", fpdf.__version__)
print("markdown:", markdown.__version__)
print("uharfbuzz imported OK")
```

---

## 5. Font Setup

The script looks for `kalpurush.ttf` in these places, in this order:

| # | Location | When it's used |
|---|---|---|
| 1 | Script / notebook folder | You copied the font next to your script |
| 2 | `C:\Windows\Fonts\` | Font installed "for all users" |
| 3 | `%LOCALAPPDATA%\Microsoft\Windows\Fonts\` | Font installed with right-click → **Install** (Windows 10/11 default) |

### Recommended setup
Copy `kalpurush.ttf` into the **same folder as your script or notebook**. This is the most reliable option, and the project stays portable.

### Unicode vs ANSI
Kalpurush comes in two versions:
- **Kalpurush (Unicode)** ✅ works with this script
- **Kalpurush ANSI** ❌ made for old Bijoy-style typing; doesn't show Unicode Bengali properly

### Finding your notebook's folder
```python
import os
print(os.getcwd())
```

---

## 6. Quick Start

1. Install the libraries (see [Installation](#4-installation)).
2. Put `kalpurush.ttf` in your working folder.
3. Store your story in a variable called `text`:
   ```python
   text = """# আমার গল্প

   এটি **প্রথম** অনুচ্ছেদ।

   এটি *দ্বিতীয়* অনুচ্ছেদ।
   """
   ```
4. Run the script.
5. `bengali_story.pdf` is created in the same folder and opens automatically.

> 💡 If `text` isn't defined, the script uses a built-in **sample story**, so you can test your setup straight away.

---

## 7. Configuration Reference

All settings are at the top of the script.

| Setting | Default | Description |
|---|---|---|
| `COLUMN_WIDTH_INCH` | `5` | Width of the text column in inches. Converted to mm (× 25.4). |
| `FONT_SIZE` | `14` | Body text size in points. Headings scale from this. |
| `LINE_HEIGHT` | `1.6` | Line spacing multiplier for paragraphs. Bengali needs extra room for vowel signs above and below letters. |
| `PAGE_FORMAT` | `"A4"` | Paper size: `"A4"`, `"Letter"`, `"Legal"`, `"A5"`, etc. |
| `TOP_MARGIN` | `20` | Top margin in mm. |
| `BOTTOM_MARGIN` | `20` | Bottom margin in mm. A new page starts when text reaches this point. |
| `SINGLE_NEWLINE_IS_PARAGRAPH` | `False` | Set to `True` if your story separates paragraphs with a single `\n`. |
| `REMOVE_CODE_FORMATTING` | `True` | Shows `` `code` `` and ```` ``` ```` blocks in Kalpurush instead of Courier, which has no Bengali letters. |
| `OUTPUT_FILENAME` | `"bengali_story.pdf"` | Name of the PDF file. |
| `OPEN_AFTER_CREATE` | `True` | Opens the PDF in your default viewer when it's done. |

### Column width examples

| Column width | Value | Side margins on A4 (210 mm) |
|---|---|---|
| 4 inches | `4` | ≈ 54.2 mm each |
| 5 inches | `5` | ≈ 41.5 mm each |
| 6 inches | `6` | ≈ 28.8 mm each |
| 7 inches | `7` | ≈ 16.1 mm each |

> ⚠️ The column must be narrower than the page. A4 is about 8.27 inches wide and Letter is 8.5 inches.

### Font size and line height guide

| Purpose | `FONT_SIZE` | `LINE_HEIGHT` |
|---|---|---|
| Compact | 12 | 1.4 |
| Standard reading | 14 | 1.6 |
| Large print | 18 | 1.7 |

---

## 8. How It Works

```
 Markdown text (text)
        │
        ▼
 ┌──────────────────────┐
 │ markdown.markdown()  │  Markdown → HTML
 └──────────────────────┘
        │
        ▼
 ┌──────────────────────┐
 │ HTML post-processing │  • <p> → <p align="justify" line-height="…">
 │                      │  • remove <code>/<pre> (optional)
 └──────────────────────┘
        │
        ▼
 ┌──────────────────────┐
 │ FPDF page setup      │  • margins centre a 5" column
 │                      │  • automatic page breaks
 │                      │  • Kalpurush registered (regular/bold/italic)
 │                      │  • text shaping ON (uharfbuzz)
 └──────────────────────┘
        │
        ▼
 ┌──────────────────────┐
 │ pdf.write_html()     │  HTML drawn inside the column
 └──────────────────────┘
        │
        ▼
   bengali_story.pdf
```

### Key ideas

**1. Centring the column**
```python
column_width = COLUMN_WIDTH_INCH * 25.4
side_margin = (pdf.w - column_width) / 2
pdf.set_margins(left=side_margin, top=TOP_MARGIN, right=side_margin)
```
`write_html()` fills the space between the left and right margins. Setting equal margins makes the content area exactly the column width, centred on the page.

**2. Text shaping**
```python
pdf.set_text_shaping(True)
```
This turns on HarfBuzz shaping. Without it, conjuncts break apart (for example, জ্ঞ shows as জ + ্ + ঞ).

**3. Justification**
```python
html = html.replace("<p>", f'<p align="justify" line-height="{LINE_HEIGHT}">')
```
Markdown creates plain `<p>` tags. Adding `align="justify"` makes fpdf2 justify each paragraph. The last line of each paragraph stays left-aligned, as is normal for justified text.

**4. Font styles**
```python
pdf.add_font("Kalpurush", style="",   fname=font_regular)
pdf.add_font("Kalpurush", style="B",  fname=font_bold)
pdf.add_font("Kalpurush", style="I",  fname=font_regular)
pdf.add_font("Kalpurush", style="BI", fname=font_bold)
```
HTML tags like `<strong>` and `<em>` ask fpdf2 for bold or italic styles. If those styles aren't registered, fpdf2 raises an error, so every style is registered even when it points to the same file.

---

## 9. Code Structure

| Section | Purpose |
|---|---|
| **SETTINGS** | All values you can change |
| **TEXT** | Uses your existing `text` variable, or the sample story if `text` isn't defined |
| **FOLDER** | Finds the script folder (`__file__`), or falls back to `os.getcwd()` in Jupyter |
| **FONTS** | `find_font()` searches 3 locations; picks regular and bold font files |
| **MARKDOWN → HTML** | Converts Markdown, adds justification and line height, removes code formatting |
| **CREATE PDF** | Page setup, margins, font registration, text shaping, `write_html()` |
| **SAVE** | Writes the PDF, prints the path and page count, optionally opens the file |

### `find_font(filename)`

| | |
|---|---|
| **Input** | Font file name, such as `"kalpurush.ttf"` |
| **Returns** | Full path as a string if found, otherwise `None` |
| **Searches** | Script folder → `C:\Windows\Fonts` → user fonts folder |

---

## 10. Supported Markdown

| Markdown | Example | PDF result |
|---|---|---|
| Heading 1–6 | `# শিরোনাম` | Larger heading text |
| Bold | `**গাঢ়**` | Bold* |
| Italic | `*তির্যক*` | Italic* |
| Bulleted list | `- বিষয়` | Bulleted list |
| Numbered list | `1. বিষয়` | Numbered list |
| Block quote | `> উক্তি` | Indented quote |
| Horizontal line | `---` | Line across the column |
| Paragraph | Blank line between blocks | New justified paragraph |
| Inline code / code block | `` `কোড` `` | Normal text (if `REMOVE_CODE_FORMATTING = True`) |
| Tables | `\| a \| b \|` | Partial support; depends on your fpdf2 version |
| Images | `![](img.png)` | Supported if the image path exists |

\* See [Known Limitations](#13-known-limitations): Kalpurush has no bold or italic version.

### Paragraph rules
In Markdown, a **single line break doesn't start a new paragraph**:

```markdown
এটি প্রথম লাইন।
এটি একই অনুচ্ছেদে যুক্ত হবে।

এটি নতুন অনুচ্ছেদ।
```

If your story uses single line breaks between paragraphs, set:
```python
SINGLE_NEWLINE_IS_PARAGRAPH = True
```

---

## 11. Customisation Recipes

### Use real bold text
Download a Bengali font family that includes a bold file, such as **Noto Sans Bengali** or **Hind Siliguri** from Google Fonts, then change:
```python
font_regular = find_font("NotoSansBengali-Regular.ttf")
font_bold    = find_font("NotoSansBengali-Bold.ttf") or font_regular
```

### Left-aligned column instead of centred
```python
side_margin = 25   # fixed 25 mm left margin
pdf.set_margins(left=side_margin, top=TOP_MARGIN,
                right=pdf.w - side_margin - column_width)
```

### US Letter paper
```python
PAGE_FORMAT = "Letter"
```

### Read the story from a file
```python
with open("story.md", encoding="utf-8") as f:
    text = f.read()
```

### Page numbers in the footer
Add this after `pdf.write_html(...)`:
```python
total = pdf.page_no()
for i in range(1, total + 1):
    pdf.page = i
    pdf.set_y(-15)
    pdf.set_font("Kalpurush", size=10)
    pdf.cell(0, 10, f"{i} / {total}", align="C")
```

### Save with a timestamp in the file name
```python
from datetime import datetime
OUTPUT_FILENAME = f"bengali_story_{datetime.now():%Y%m%d_%H%M%S}.pdf"
```

---

## 12. Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `NameError: name '__file__' is not defined` | Running in Jupyter with an older version of the script | Use the current script (it includes a `try/except` fallback) |
| `FileNotFoundError: kalpurush.ttf not found` | Font isn't in any searched location | Copy the font into the folder shown by `os.getcwd()` |
| `ModuleNotFoundError: No module named 'fpdf'` / `'markdown'` / `'uharfbuzz'` | Library missing in the current environment | Run `%pip install fpdf2 uharfbuzz markdown`, then restart the kernel |
| Conjuncts look broken (জ + ্ + ঞ) | Text shaping is off or `uharfbuzz` is missing | Install `uharfbuzz`; check that `pdf.set_text_shaping(True)` is present |
| Squares (□) or missing letters | Wrong font (ANSI version) or Bengali inside code blocks | Use Unicode Kalpurush; set `REMOVE_CODE_FORMATTING = True` |
| Error mentioning font style `B` / `I` | Bold or italic style not registered | Keep all four `add_font(...)` lines |
| `line-height` ignored or causes an error | fpdf2 version is too old | Upgrade fpdf2, or remove ` line-height="{LINE_HEIGHT}"` |
| Justification not applied or uneven spacing | Older fpdf2 handles shaped justified text less well | `%pip install --upgrade fpdf2`, then restart the kernel |
| `PermissionError` when saving | The PDF is still open in a viewer | Close the PDF and run again |
| Paragraphs run together | Single `\n` between paragraphs | Set `SINGLE_NEWLINE_IS_PARAGRAPH = True` |
| Vowel signs cramped or overlapping between lines | Line spacing too small | Increase `LINE_HEIGHT` (for example `1.8`) |
| Conflicting or strange behaviour after install | Old `fpdf` and new `fpdf2` both installed | `pip uninstall fpdf fpdf2`, then `pip install fpdf2` |

### Diagnostic snippet
```python
import os, fpdf
print("Working folder:", os.getcwd())
print("fpdf2 version :", fpdf.__version__)
print("Font in folder:", os.path.exists("kalpurush.ttf"))
```

---

## 13. Known Limitations

1. **No real bold or italic with Kalpurush.** The font has only one weight, so bold and italic text looks like normal text. Use a font family with a bold file if you need it. True italic Bengali fonts are rare.
2. **Code blocks lose monospace formatting** when `REMOVE_CODE_FORMATTING = True`. This is deliberate, so Bengali in code blocks still displays.
3. **Only paragraphs are justified.** Headings, list items and quotes use their default alignment.
4. **Limited HTML/CSS support.** `write_html()` handles a subset of HTML. Complex Markdown such as nested tables or footnotes may not look exactly as expected.
5. **Windows-specific features.** `os.startfile()` and the font paths are for Windows. On macOS or Linux, remove `os.startfile()` and keep the font in the script folder.
6. **No hyphenation.** Long words aren't split at line ends, which can make word spacing in narrow justified columns look uneven.

---

## 14. FAQ

**Q: Can I mix English and Bengali?**
Yes. Kalpurush includes basic Latin letters. For better-looking English text, use a font family that covers both scripts, such as Noto Sans Bengali.

**Q: Does it handle very long stories?**
Yes. Automatic page breaks start new pages as needed, and the column width stays the same on every page.

**Q: Can I change the column width to centimetres?**
Yes. Replace the conversion line with a value in mm, for example `column_width = 12 * 10` for 12 cm.

**Q: Can this be built into a tkinter app?**
Yes. Put the PDF-creation part inside a function that takes `text` as a parameter, and call it from a button command.

**Q: Why HTML instead of drawing Markdown directly?**
fpdf2 doesn't read full Markdown. Converting to HTML first gives proper support for headings, lists and quotes.

---

*Built with fpdf2, uharfbuzz, Python-Markdown and the Kalpurush font.*
