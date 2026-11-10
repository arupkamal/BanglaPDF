import os
import markdown
from fpdf import FPDF

# =====================================================================
# SETTINGS
# =====================================================================
COLUMN_WIDTH_INCH = 5          # Column width in inches
FONT_SIZE = 14                 # Body text size
LINE_HEIGHT = 1.6              # Line spacing (1.0 = tight, 1.6 = comfortable for Bengali)
PAGE_FORMAT = "A4"             # "A4" or "Letter"
TOP_MARGIN = 20                # mm
BOTTOM_MARGIN = 20             # mm
SINGLE_NEWLINE_IS_PARAGRAPH = False   # True if your story separates paragraphs with a single \n
REMOVE_CODE_FORMATTING = True         # Show `code` / ``` blocks in Kalpurush instead of Courier
OUTPUT_FILENAME = "bengali_story.pdf"
OPEN_AFTER_CREATE = True

# =====================================================================
# TEXT (uses your existing `text` variable if it's already defined)
# =====================================================================
try:
    text
except NameError:
    text = """# বিজ্ঞান ও প্রযুক্তি মন্ত্রণালয়

## প্রথম অধ্যায়

এটি একটি **নমুনা গল্প**। এখানে *মার্কডাউন* ফরম্যাটিং পরীক্ষা করা হচ্ছে। বিজ্ঞান ও প্রযুক্তি আমাদের জীবনকে প্রতিনিয়ত বদলে দিচ্ছে, আর সেই পরিবর্তনের গল্পই এখানে বলা হবে।

> জ্ঞানই শক্তি।

- প্রথম বিষয়
- দ্বিতীয় বিষয়
- তৃতীয় বিষয়

---

গল্পের শেষ অনুচ্ছেদ এখানে। সম্পূর্ণ জাস্টিফাইড অ্যালাইনমেন্টে লেখাটি দেখা যাবে।
"""

# =====================================================================
# FOLDER (works in both Jupyter and .py scripts)
# =====================================================================
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    script_dir = os.getcwd()

# =====================================================================
# FONTS
# =====================================================================
def find_font(filename):
    candidates = [
        os.path.join(script_dir, filename),
        os.path.join(r"C:\Windows\Fonts", filename),
        os.path.join(os.environ.get("LOCALAPPDATA", ""),
                     r"Microsoft\Windows\Fonts", filename),
    ]
    for f in candidates:
        if os.path.exists(f):
            return f
    return None

font_regular = find_font("kalpurush.ttf")
if font_regular is None:
    raise FileNotFoundError(
        "kalpurush.ttf not found. Put it in this folder or install it in Windows:\n"
        + script_dir
    )

# Kalpurush has only one weight. If you have a real bold Bengali font,
# change the file name below. Otherwise the regular font is used.
font_bold = find_font("kalpurush-bold.ttf") or font_regular

print("Regular font:", font_regular)
print("Bold font   :", font_bold)

# =====================================================================
# MARKDOWN -> HTML
# =====================================================================
if SINGLE_NEWLINE_IS_PARAGRAPH:
    text = text.replace("\r\n", "\n").replace("\n", "\n\n")

html = markdown.markdown(text, extensions=["extra", "sane_lists"])

# Make paragraphs fully justified with comfortable line spacing
html = html.replace("<p>", f'<p align="justify" line-height="{LINE_HEIGHT}">')

# Courier has no Bengali letters, so turn code blocks into normal text
if REMOVE_CODE_FORMATTING:
    html = (html.replace("<pre>", "<p>").replace("</pre>", "</p>")
                .replace("<code>", "").replace("</code>", ""))

# =====================================================================
# CREATE PDF
# =====================================================================
pdf = FPDF(orientation="P", unit="mm", format=PAGE_FORMAT)

column_width = COLUMN_WIDTH_INCH * 25.4          # inches -> mm
side_margin = (pdf.w - column_width) / 2         # centre the column
pdf.set_margins(left=side_margin, top=TOP_MARGIN, right=side_margin)
pdf.set_auto_page_break(auto=True, margin=BOTTOM_MARGIN)
pdf.add_page()

# Register every style the HTML might ask for
pdf.add_font("Kalpurush", style="",   fname=font_regular)
pdf.add_font("Kalpurush", style="B",  fname=font_bold)
pdf.add_font("Kalpurush", style="I",  fname=font_regular)
pdf.add_font("Kalpurush", style="BI", fname=font_bold)

pdf.set_font("Kalpurush", size=FONT_SIZE)
pdf.set_text_shaping(True)                       # Correct Bengali conjuncts

pdf.write_html(html, font_family="Kalpurush")

# =====================================================================
# SAVE
# =====================================================================
output_file = os.path.join(script_dir, OUTPUT_FILENAME)
pdf.output(output_file)
print("PDF created:", output_file)
print("Total pages:", pdf.page_no())

if OPEN_AFTER_CREATE:
    os.startfile(output_file)
