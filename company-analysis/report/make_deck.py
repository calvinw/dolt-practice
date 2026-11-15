"""Build company_comparison.pptx: Ross vs TJ Maxx, fiscal year 2024.

Run from the report folder:  python3 make_deck.py
Charts are read from charts/, numbers from analysis.md / data_2024.csv.
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

NAVY = RGBColor(0x1F, 0x4E, 0x79)
RED = RGBColor(0xC0, 0x00, 0x00)
DARK = RGBColor(0x22, 0x22, 0x22)
GREY = RGBColor(0x66, 0x66, 0x66)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def add_title(text, color=NAVY):
    slide = prs.slides.add_slide(BLANK)
    box = slide.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(12.1), Inches(0.9))
    p = box.text_frame.paragraphs[0]
    p.text = text
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = color
    return slide


def add_bullets(slide, items, left=0.8, top=1.4, width=11.7, height=5.4, size=18):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        level = 0
        if isinstance(item, tuple):
            item, level = item
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = ("• " if level == 0 else "– ") + item
        p.level = level
        p.font.size = Pt(size if level == 0 else size - 2)
        p.font.color.rgb = DARK if level == 0 else GREY
        p.space_after = Pt(8)
    return tf


def add_table(slide, headers, rows, left, top, width, height, size=16):
    shape = slide.shapes.add_table(len(rows) + 1, len(headers), Inches(left),
                                   Inches(top), Inches(width), Inches(height))
    table = shape.table
    for j, h in enumerate(headers):
        c = table.cell(0, j)
        c.text = h
        c.text_frame.paragraphs[0].font.size = Pt(size)
        c.text_frame.paragraphs[0].font.bold = True
        c.text_frame.paragraphs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        c.fill.solid()
        c.fill.fore_color.rgb = NAVY
    for i, row in enumerate(rows, start=1):
        for j, val in enumerate(row):
            c = table.cell(i, j)
            c.text = str(val)
            c.text_frame.paragraphs[0].font.size = Pt(size)
            c.text_frame.paragraphs[0].font.color.rgb = DARK
    return table


def add_chart_slide(title, image, caption, slide=None):
    if slide is None:
        slide = add_title(title)
    else:
        box = slide.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(12.1), Inches(0.9))
        p = box.text_frame.paragraphs[0]
        p.text = title
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = NAVY
    pic = slide.shapes.add_picture(image, Inches(0), Inches(1.3), height=Inches(4.9))
    pic.left = int((prs.slide_width - pic.width) / 2)  # centre horizontally
    cap = slide.shapes.add_textbox(Inches(0.8), Inches(6.35), Inches(11.7), Inches(0.9))
    tf = cap.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = caption
    p.font.size = Pt(15)
    p.font.color.rgb = GREY
    return slide


# --- Slide 1: title -----------------------------------------------------
s = prs.slides.add_slide(BLANK)
box = s.shapes.add_textbox(Inches(0.8), Inches(2.3), Inches(11.7), Inches(1.4))
p = box.text_frame.paragraphs[0]
p.text = "Ross vs TJ Maxx"
p.font.size = Pt(54)
p.font.bold = True
p.font.color.rgb = NAVY
box = s.shapes.add_textbox(Inches(0.8), Inches(3.5), Inches(11.7), Inches(1.2))
tfp = box.text_frame
tfp.word_wrap = True
p = tfp.paragraphs[0]
p.text = "A financial comparison of two off-price retailers"
p.font.size = Pt(26)
p.font.color.rgb = DARK
p = tfp.add_paragraph()
p.text = "Fiscal year 2024  |  Source: BusMgmtBenchmarks (Dolt)"
p.font.size = Pt(16)
p.font.color.rgb = GREY

# --- Slide 2: the two companies ----------------------------------------
s = add_title("The two companies")
add_bullets(s, [
    "TJ Maxx (ticker TJX) and Ross (ticker ROST) are both off-price retailers.",
    "Off-price means buying brand-name goods cheaply and selling them at a discount.",
    ("Same segment in the database: Off Price — a fair comparison.", 1),
    ("Both report in US dollars, in thousands — so amounts can be compared directly.", 1),
    "TJ Maxx sells off-price apparel and home fashions.",
    "Ross sells off-price apparel, accessories and footwear.",
    "Year compared: fiscal 2024 (both years ended 2025-02-01).",
])

# --- Slide 3: headline numbers -----------------------------------------
s = add_title("The headline numbers (fiscal 2024)")
add_table(
    s,
    ["Measure", "TJ Maxx", "Ross"],
    [
        ["Net revenue", "$56.4 billion", "$21.1 billion"],
        ["Net profit", "$4.86 billion", "$2.09 billion"],
        ["Net profit margin", "8.63%", "9.90%"],
        ["Operating margin", "11.50%", "12.24%"],
        ["Gross margin", "30.60%", "27.78%"],
    ],
    left=1.6, top=1.5, width=10.1, height=3.6,
)
box = s.shapes.add_textbox(Inches(1.6), Inches(5.4), Inches(10.1), Inches(1.4))
tfp = box.text_frame
tfp.word_wrap = True
p = tfp.paragraphs[0]
p.text = ("TJ Maxx is about 2.7x larger by revenue, yet Ross keeps more of each "
          "sales dollar as profit.")
p.font.size = Pt(16)
p.font.color.rgb = GREY

# --- Slides 4-9: charts -------------------------------------------------
add_chart_slide(
    "Size: net revenue",
    "charts/net_revenue.png",
    "TJ Maxx's revenue ($56.4B) is about 2.7 times Ross's ($21.1B). Revenue only "
    "shows size, not how well each company turns sales into profit.",
)
add_chart_slide(
    "Profitability: margins",
    "charts/profit_margins.png",
    "TJ Maxx wins at the gross margin line (30.6% vs 27.8%), but Ross wins on "
    "operating (12.2% vs 11.5%) and net margin (9.9% vs 8.6%) — so Ross keeps "
    "more profit per sales dollar.",
)
add_chart_slide(
    "Why Ross is leaner: overhead",
    "charts/sga_pct.png",
    "SG&A (running stores and head office) is 15.5% of sales at Ross vs 19.4% at "
    "TJ Maxx. That ~4-point gap is why Ross is more profitable per sale.",
)
add_chart_slide(
    "Inventory efficiency",
    "charts/inventory_turnover.png",
    "A near tie: Ross turns inventory 6.24 times a year vs TJ Maxx's 6.09. "
    "Faster turns mean less stock must be marked down.",
)
add_chart_slide(
    "Return on assets — and why",
    "charts/roa_decomposition.png",
    "TJ Maxx's ROA is higher (15.3% vs 14.0%). ROA = net margin x asset "
    "turnover: Ross wins on margin, but TJ Maxx turns its assets harder "
    "(1.78 vs 1.42), which wins overall.",
)
add_chart_slide(
    "Financial health",
    "charts/financial_health.png",
    "Ross is stronger: a higher current ratio (1.62 vs 1.18) means more cushion "
    "to pay short-term bills, and lower debt to equity (1.71 vs 2.78) means less "
    "reliance on borrowed money.",
)

# --- Slide 10: key findings --------------------------------------------
s = add_title("Key findings")
add_bullets(s, [
    "TJ Maxx is much bigger: $56.4B revenue vs Ross's $21.1B.",
    "Ross is more profitable per sale: 9.9% net margin vs 8.6%.",
    "The difference is overhead: Ross's SG&A is 15.5% of sales vs 19.4%.",
    "Inventory is a near tie; Ross turns stock slightly faster (6.24 vs 6.09).",
    "TJ Maxx earns a higher return on assets (15.3% vs 14.0%) by turning its "
    "assets harder, not by keeping more margin.",
    "Ross has the safer balance sheet — more liquidity, less debt.",
], size=19)

# --- Slide 11: verdict --------------------------------------------------
s = add_title("The verdict: which is stronger?")
add_bullets(s, [
    "It depends on what you mean by stronger — but overall, Ross looks the "
    "healthier business.",
    ("Ross is more profitable on every sale, is leaner, and carries less debt.", 1),
    ("TJ Maxx is bigger and squeezes more sales from its assets.", 1),
    "In plain words: TJ Maxx makes more money by being large; Ross makes more "
    "money on each sale and is in better financial shape.",
], size=20)

prs.save("company_comparison.pptx")
print("wrote company_comparison.pptx with", len(prs.slides.__iter__.__self__._sldIdLst), "slides")
