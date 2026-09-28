"""Build the public, two-page academic CV.

Run with the bundled Codex Python runtime (reportlab required):
    python scripts/build_cv.py assets/cv/CV_XinhaoDong.pdf
"""

import argparse
from html import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


PAGE_W, PAGE_H = 612, 792
LEFT, RIGHT, TOP, BOTTOM = 47, 47, 43, 42
WIDTH = PAGE_W - LEFT - RIGHT
INK = colors.HexColor("#24312F")
ACCENT = colors.HexColor("#3F665C")
MUTED = colors.HexColor("#58645F")
RULE = colors.HexColor("#CCD4CD")
SITE = "https://xinhaodong.github.io/"

body = ParagraphStyle(
    "body", fontName="Times-Roman", fontSize=9.35, leading=12.1,
    textColor=INK, alignment=TA_LEFT, spaceAfter=0,
)
small = ParagraphStyle(
    "small", parent=body, fontSize=8.9, leading=11.5, textColor=MUTED,
)
title_style = ParagraphStyle(
    "title", parent=body, fontName="Times-Bold", fontSize=9.9,
    leading=12.8,
)


def draw_paragraph(pdf, markup, y, style=body, indent=0):
    paragraph = Paragraph(markup, style)
    _, height = paragraph.wrap(WIDTH - indent, PAGE_H)
    paragraph.drawOn(pdf, LEFT + indent, y - height)
    return y - height


def section(pdf, label, y):
    y -= 12
    pdf.setFillColor(ACCENT)
    pdf.setFont("Helvetica-Bold", 9.4)
    pdf.drawString(LEFT, y, label.upper())
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(0.55)
    pdf.line(LEFT, y - 5, PAGE_W - RIGHT, y - 5)
    return y - 17


def entry(pdf, title, detail, y, link=None, note=None):
    safe_title = escape(title)
    if link:
        safe_title = f'<link href="{escape(link)}" color="#3F665C">{safe_title}</link>'
    y = draw_paragraph(pdf, safe_title, y, title_style)
    if detail:
        y = draw_paragraph(pdf, escape(detail), y - 1, small)
    if note:
        y = draw_paragraph(pdf, escape(note), y - 1, small)
    return y - 22


def two_column(pdf, left, right, y, second=None):
    pdf.setFont("Times-Bold", 9.55)
    pdf.setFillColor(INK)
    pdf.drawString(LEFT, y, left)
    pdf.setFont("Times-Roman", 9.0)
    pdf.setFillColor(MUTED)
    pdf.drawRightString(PAGE_W - RIGHT, y, right)
    y -= 13
    if second:
        y = draw_paragraph(pdf, escape(second), y, small) - 2
    return y - 9


def footer(pdf, page):
    pdf.setStrokeColor(RULE)
    pdf.line(LEFT, 36, PAGE_W - RIGHT, 36)
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 7.8)
    pdf.drawString(LEFT, 24, "Xinhao Dong | September 2026")
    pdf.drawRightString(PAGE_W - RIGHT, 24, str(page))


def build(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_W, PAGE_H), pageCompression=1)
    pdf.setTitle("Curriculum Vitae - Xinhao Dong")
    pdf.setAuthor("Xinhao Dong")
    pdf.setSubject("Academic curriculum vitae")

    y = PAGE_H - TOP
    pdf.setFillColor(INK)
    pdf.setFont("Times-Bold", 20)
    pdf.drawString(LEFT, y, "Xinhao Dong (Jack)")
    y -= 18
    pdf.setFont("Helvetica", 8.8)
    pdf.drawString(LEFT, y, "PhD Candidate in Economics  |  Simon Fraser University")
    y -= 14
    pdf.drawString(LEFT, y, "xinhao_dong@sfu.ca  |  +1 778-862-7719  |  xinhaodong.github.io")
    pdf.linkURL("mailto:xinhao_dong@sfu.ca", (LEFT, y - 2, LEFT + 105, y + 9), relative=0)
    pdf.linkURL(SITE, (LEFT + 255, y - 2, PAGE_W - RIGHT, y + 9), relative=0)

    y = section(pdf, "Education", y)
    y = two_column(pdf, "PhD in Economics, Simon Fraser University", "2023-present", y,
                   "Supervisor: Lucas Herrenbrueck")
    y = two_column(pdf, "MA in Economics, Simon Fraser University", "2022-2023", y)
    y = two_column(pdf, "BA in Mathematics and Economics, University of British Columbia", "2018-2021", y)

    y = section(pdf, "Working Papers", y)
    papers = [
        ("Deposit Pricing, Bank Funding Models, and the Incidence of Reserve Requirements",
         "Compares bank-funding gradients across deposit-pricing regimes in China; earlier version presented as Financial Liberalization and the Effectiveness of Reserve Policy.",
         "assets/papers/deposit-pricing-reserve-requirements.pdf", None),
        ("Urgency, Liquidity, and the Price of Convenience",
         "With Lucas Herrenbrueck and Zijian Wang. Estimates the value of asset convenience while separating marketability from the urgency of spending needs.",
         "assets/papers/urgency-liquidity-price-of-convenience.pdf", None),
        ("Existing Credit, New Credit, and Monetary Transmission",
         "Shows that monetary tightening reprices card borrowing and limits new credit, while authorized credit on existing accounts remains largely unchanged.",
         "assets/papers/existing-credit-new-credit-monetary-transmission.pdf", None),
        ("Who Gets Protection? Geographic Inequality in Social Protection after Land Expropriation in China",
         "Documents how the geographic gradient in durable protection for land-losing households weakened across expropriation cohorts.",
         "assets/papers/who-gets-protection.pdf", None),
        ("Pensions, Migration, and Three-Generation Family Reorganization",
         "With Yang Li. Examines pension eligibility, grandchild care, migration, and family transfers in rural China.",
         "https://www.dropbox.com/scl/fi/l6o3wmeur9fnl1vhy168h/Rural_Pension.pdf?rlkey=k0lvzd16sgpemzimauc0o3s40&st=vspo28mm&dl=0", None),
        ("Strategic Obfuscation against Adaptive Censorship: Equilibrium Blocking and Dynamic Implementability",
         "With Yuqi Hu. Models blocking and costly obfuscation in static and repeated strategic interactions.",
         "assets/papers/strategic-obfuscation-adaptive-censorship.pdf", None),
    ]
    for name, summary, href, note in papers:
        target = SITE + href if href and not href.startswith("https://") else href
        y = entry(pdf, name, summary, y, target, note)

    y = section(pdf, "Work in Progress", y)
    y = entry(pdf, "State or Type? Revolving Debt and Household Payment Choice",
              "Studies debt state and persistent household preferences in credit-card payment choice.", y)
    y = entry(pdf, "The Structure and Selective Compression of Central-Bank Information",
              "Studies how PBoC policy information is selected and represented by professional intermediaries.", y)
    if y < BOTTOM + 10:
        raise RuntimeError(f"CV page 1 overflow: {y:.1f}")
    footer(pdf, 1)
    pdf.showPage()

    y = PAGE_H - TOP
    y = section(pdf, "Conference and Seminar Presentations", y)
    y = draw_paragraph(pdf,
                       "<b>Deposit Pricing, Bank Funding Models, and the Incidence of Reserve Requirements</b>"
                       " (earlier version presented under its former title)", y, body) - 8
    venues = [
        ("2026", "Chinese Economists Society (CES) China Annual Conference, Chengdu | July 3-5"),
        ("2026", "Econometric Society Asia Meeting-China, Hong Kong | June 19-21"),
        ("2026", "Econometric Society North American Summer Meeting, Atlanta | June 4-7"),
        ("2026", "60th Annual Meetings of the Canadian Economics Association, SFU | May 28-30"),
        ("2026", "Econometric Society Asia Meeting, Abu Dhabi"),
        ("2025", "Econometric Society European Winter Meeting, Nicosia"),
        ("2025", "Simon Fraser University; University of British Columbia"),
    ]
    for year, venue in venues:
        y = draw_paragraph(pdf, f'<font color="#3F665C"><b>{year}</b></font>  {escape(venue)}', y, body, 5) - 4

    y = section(pdf, "Research Experience", y)
    y = two_column(pdf, "Research Assistant, Simon Fraser University", "2024-present", y,
                   "Research with Lucas Herrenbrueck on liquidity pricing.")
    y = two_column(pdf, "Research Assistant, Simon Fraser University", "2023-2024", y,
                   "Research with Serena Canaan on adviser religion and student outcomes.")
    y = two_column(pdf, "Research Assistant, UBC Vancouver School of Economics", "2020", y,
                   "Research with Li Hao on Nash equilibrium in penalty shootouts.")

    y = section(pdf, "Teaching Experience", y)
    y = two_column(pdf, "Teaching Assistant, Simon Fraser University", "2022-present", y,
                   "Microeconomics (Econ 103, 201, 302, 802); macroeconomics (Econ 807); industrial organization (Econ 325); public economics (Econ 392).")

    y = section(pdf, "Fellowships, Honors, and Awards", y)
    awards = [
        "Peter Kennedy Memorial Graduate Fellowship (2026)",
        "Lang Wong Memorial Scholarship in Economics, Simon Fraser University (2025)",
        "FASS Research Travel Award, Simon Fraser University (2025)",
        "PhD Research Scholarship, Simon Fraser University (2023-2025)",
        "Supplemental Graduate Fellowship, Simon Fraser University (2025)",
        "Special Graduate Entrance Scholarship, Simon Fraser University (2024)",
    ]
    for award in awards:
        y = draw_paragraph(pdf, escape(award), y, body, 5) - 5

    y = section(pdf, "Languages and Tools", y)
    y = draw_paragraph(pdf, "Mandarin (native); English (fluent). R, Stata, Python, LaTeX.", y, body)
    if y < BOTTOM + 10:
        raise RuntimeError(f"CV page 2 overflow: {y:.1f}")
    footer(pdf, 2)
    pdf.save()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    build(parser.parse_args().output)
