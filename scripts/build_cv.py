"""Build the public academic CV with ReportLab."""

import argparse
from html import escape
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

W, H = 612, 792
L, R, TOP, BOTTOM = 71, 71, 57, 46
TEXT_W = W - L - R
SITE = "https://xinhaodong.github.io/"
BLACK = colors.black

body = ParagraphStyle("body", fontName="Times-Roman", fontSize=10.15,
                      leading=12.7, textColor=BLACK)
title = ParagraphStyle("title", parent=body, fontName="Times-Bold",
                       fontSize=10.45, leading=12.8)
detail = ParagraphStyle("detail", parent=body, fontName="Times-Italic",
                        fontSize=9.55, leading=11.8)
compact = ParagraphStyle("compact", parent=body, fontSize=10, leading=12.3)


def para(pdf, value, y, style=body, indent=0):
    block = Paragraph(value, style)
    _, height = block.wrap(TEXT_W - indent, H)
    block.drawOn(pdf, L + indent, y - height)
    return y - height


def section(pdf, label, y, gap=18):
    y -= gap
    pdf.setFont("Times-Bold", 11.7)
    pdf.drawString(L, y, label)
    return y - 11


def education(pdf, school, location, degree, dates, y, supervisor=False):
    y -= 9
    pdf.setFont("Times-Bold", 10.2)
    pdf.drawString(L, y, school)
    school_width = pdf.stringWidth(school, "Times-Bold", 10.2)
    pdf.setFont("Times-Roman", 10)
    pdf.drawString(L + school_width, y, ", " + location)
    pdf.drawRightString(W - R, y, dates)
    y -= 13
    pdf.drawString(L, y, degree)
    if supervisor:
        y -= 13
        pdf.drawString(L, y, "Supervisor: Lucas Herrenbrueck")
    return y - 7


def paper(pdf, name, summary, y, authors=None, link=None, note=None, gap=11):
    y -= gap
    label = escape(name)
    if link:
        label = f'<link href="{escape(link)}" color="#000000">{label}</link>'
    y = para(pdf, label, y, title)
    if authors:
        y = para(pdf, escape("with " + authors), y - 1, detail)
    if note:
        y = para(pdf, escape(note), y - 1, detail)
    return para(pdf, escape(summary), y - 2)


def line(pdf, value, y, indent=0, style=compact):
    return para(pdf, escape(value), y, style, indent)


def experience(pdf, institution, dates, description, y):
    y -= 10
    role, _, organization = institution.partition(", ")
    pdf.setFont("Times-Bold", 10.1)
    pdf.drawString(L, y, role)
    role_width = pdf.stringWidth(role, "Times-Bold", 10.1)
    pdf.setFont("Times-Roman", 10.1)
    pdf.drawString(L + role_width, y, ", " + organization)
    pdf.drawRightString(W - R, y, dates)
    return line(pdf, description, y - 3) - 5


def subsection(pdf, label, y, gap=11):
    y -= gap
    pdf.setFont("Times-Bold", 10.45)
    pdf.drawString(L, y, label)
    return y - 8


def venue(pdf, year, name, y):
    y -= 4
    pdf.setFont("Times-Roman", 10)
    pdf.drawString(L + 10, y - 10, year)
    return para(pdf, escape(name), y, compact, 49) - 2


def footer(pdf, page):
    pdf.setFont("Times-Roman", 9)
    pdf.drawCentredString(W / 2, 30, str(page))


def contact_line(pdf, y):
    font, size = "Times-Roman", 10.3
    email = "xinhao_dong@sfu.ca"
    phone = "+1 778-862-7719"
    website = "xinhaodong.github.io"
    separator = "  |  "
    pieces = [email, separator, phone, separator, website]
    widths = [pdf.stringWidth(piece, font, size) for piece in pieces]
    x = (W - sum(widths)) / 2
    pdf.setFont(font, size)
    for piece, width in zip(pieces, widths):
        pdf.drawString(x, y, piece)
        if piece == email:
            pdf.linkURL("mailto:" + email, (x, y - 2, x + width, y + size))
        elif piece == website:
            pdf.setLineWidth(0.45)
            pdf.line(x, y - 1.3, x + width, y - 1.3)
            pdf.linkURL(SITE, (x, y - 2, x + width, y + size))
        x += width


def build(path):
    pdf = canvas.Canvas(path, pagesize=(W, H), pageCompression=1)
    pdf.setTitle("Curriculum Vitae - Xinhao Dong")
    pdf.setAuthor("Xinhao Dong")
    pdf.setSubject("Academic curriculum vitae")

    y = H - TOP
    pdf.setFont("Times-Bold", 16.8)
    pdf.drawCentredString(W / 2, y, "Xinhao Dong (Jack)")
    y -= 20
    contact_line(pdf, y)

    y = section(pdf, "Education", y, 24)
    y = education(pdf, "Simon Fraser University", "Vancouver, BC, Canada",
                  "Doctor of Philosophy, Economics", "09/2023 – Present", y, True)
    y = education(pdf, "Simon Fraser University", "Vancouver, BC, Canada",
                  "Master of Arts, Economics", "09/2022 – 08/2023", y)
    y = education(pdf, "University of British Columbia", "Vancouver, BC, Canada",
                  "Bachelor of Arts, Mathematics and Economics",
                  "09/2018 – 06/2021", y)
    y = section(pdf, "Research", y, 21)
    y = section(pdf, "Working Papers", y, 13)
    y = paper(pdf,
        "Deposit Pricing, Bank Funding Models, and the Incidence of Reserve Requirements",
        "Using quarterly data on 14 nationwide Chinese banks, I compare the relationship "
        "between reserve requirements and market funding before and after deposit-rate "
        "ceiling removal. Among joint-stock banks, the positive pre-removal funding "
        "gradient is nearly zero afterward. Limited common support and sensitivity to "
        "exposure trends preclude a causal interpretation of this regime difference.",
        y, link=SITE + "assets/papers/deposit-pricing-reserve-requirements.pdf",
        note="Earlier version: Financial Liberalization and the Effectiveness of Reserve "
             "Policy: Evidence from China's 2015 Deposit Rate Reform.")
    y = paper(pdf, "Urgency, Liquidity, and the Price of Convenience",
        "A monetary asset-pricing model separates the value of liquidity from the urgency "
        "of spending needs. Using Treasury bills, commercial paper, and AAA corporate "
        "bonds, we estimate an average annual price of convenience of 5.5 percent; "
        "urgency accounts for 23 percent of it on average.",
        y, authors="Lucas Herrenbrueck and Zijian Wang",
        link=SITE + "assets/papers/urgency-liquidity-price-of-convenience.pdf")
    y = paper(pdf, "Existing Credit, New Credit, and Monetary Transmission",
        "Using U.S. credit-card market data and high-frequency monetary surprises, "
        "I distinguish the pricing of existing debt, limits on new accounts, and "
        "credit already authorized on open accounts. Tightening raises borrowing "
        "rates and weakens initial limits, but does not contract existing lines "
        "across four measured margins; households instead increase utilization "
        "and delinquency.",
        y, link=SITE + "assets/papers/existing-credit-new-credit-monetary-transmission.pdf")
    y = paper(pdf,
        "Who Gets Protection? Geographic Inequality in Social Protection after Land Expropriation in China",
        "Using rural China Household Income Project surveys, I compare compensation "
        "received by land-losing households across provinces and expropriation "
        "cohorts. Earlier cohorts in fiscally weaker provinces were less likely "
        "to receive continuing social protection and more likely to receive cash "
        "alone; these gaps largely closed among later cohorts, while cross-province "
        "dispersion fell by about one-third.",
        y, link=SITE + "assets/papers/who-gets-protection.pdf")
    y = paper(pdf, "Pensions, Migration, and Three-Generation Family Reorganization",
        "Using age-60 eligibility around China's 2016 pension reform, we find "
        "that pension access raises grandparents' childcare by 8.2 percentage "
        "points. Grandchildren spend fewer months with their parents, while "
        "migration shifts toward shorter, more returnable trips. Remittances "
        "from pension recipients to adult children fall, consistent with "
        "a change in how families share care and financial support.",
        y, authors="Yang Li",
        link="https://www.dropbox.com/scl/fi/l6o3wmeur9fnl1vhy168h/Rural_Pension.pdf?rlkey=k0lvzd16sgpemzimauc0o3s40&st=vspo28mm&dl=0")
    if y < BOTTOM + 5:
        raise RuntimeError(f"CV page 1 overflow: y={y:.1f}")
    footer(pdf, 1)
    pdf.showPage()

    y = H - TOP
    y = section(pdf, "Working Papers (continued)", y, 0)
    y = paper(pdf,
        "Strategic Obfuscation against Adaptive Censorship: Equilibrium Blocking and Dynamic Implementability",
        "We model a censorship-resistance operator's costly obfuscation and an adaptive "
        "censor's blocking choice. The static game characterizes their joint response; "
        "the repeated game derives conditions under which obfuscation can be sustained "
        "against each player's exact unilateral deviation. Classification errors and "
        "imperfect public signals further tighten those conditions.",
        y, authors="Yuqi Hu",
        link=SITE + "assets/papers/strategic-obfuscation-adaptive-censorship.pdf")
    y = section(pdf, "Work in Progress", y, 25)
    y = paper(pdf, "State or Type? Revolving Debt and Household Payment Choice",
        "Using linked U.S. consumer payment surveys and transaction diaries, this project "
        "asks whether the lower credit-card payment share of households carrying card debt "
        "reflects their current revolving state or persistent differences in payment "
        "behavior. It compares payment choices within households and across households.",
        y, gap=3)
    y = paper(pdf,
        "The Structure and Selective Compression of Central-Bank Information: "
        "Evidence from PBoC Reports and Professional Intermediaries",
        "Using PBoC Monetary Policy Implementation Reports and professional articles "
        "around their release, this project traces how central-bank statements are "
        "selected and summarized. It examines selection into coverage separately "
        "from whether reports preserve policy instruments, direction, magnitudes, "
        "and timing.",
        y, gap=13)

    y = section(pdf, "Conference and Seminar Presentations", y, 25)
    y = line(pdf, "Financial Liberalization and the Effectiveness of Reserve Policy: "
        "Evidence from China's 2015 Deposit Rate Reform (earlier version)",
        y - 5, 0, title)
    y = subsection(pdf, "Conferences", y, 11)
    conferences = [
        ("2026", "Chinese Economists Society (CES) China Annual Conference, Chengdu"),
        ("2026", "Econometric Society Asia Meeting–China, Hong Kong"),
        ("2026", "Econometric Society North American Summer Meeting, Atlanta"),
        ("2026", "Canadian Economics Association Annual Meetings, Simon Fraser University"),
        ("2026", "Econometric Society Asia Meeting, Abu Dhabi"),
        ("2025", "Econometric Society European Winter Meeting, Nicosia"),
    ]
    for year, name in conferences:
        y = venue(pdf, year, name, y)
    y = subsection(pdf, "Seminars", y, 14)
    for name in [
        "NYU Shanghai",
        "Simon Fraser University",
        "University of British Columbia",
    ]:
        y = venue(pdf, "2025", name, y)
    if y < BOTTOM + 5:
        raise RuntimeError(f"CV page 2 overflow: y={y:.1f}")
    footer(pdf, 2)
    pdf.showPage()

    y = H - TOP
    y = section(pdf, "Research Experience", y, 0)
    y = experience(pdf, "Research Assistant, Simon Fraser University",
        "06/2024 – Present", "Research with Lucas Herrenbrueck on liquidity pricing.", y)
    y = experience(pdf, "Research Assistant, Simon Fraser University",
        "06/2023 – 01/2024",
        "Research with Serena Canaan on adviser religion and student outcomes.", y)
    y = experience(pdf, "Research Assistant, UBC Vancouver School of Economics",
        "01/2020 – 09/2020",
        "Research with Li Hao on Nash equilibrium in penalty shootouts.", y)
    y = section(pdf, "Teaching Experience", y, 22)
    y = experience(pdf, "Teaching Assistant, Simon Fraser University",
        "09/2022 – Present",
        "Microeconomics (Econ 103, 201, 302, 802); macroeconomics (Econ 807); "
        "industrial organization (Econ 325); public economics (Econ 392).", y)

    y = section(pdf, "Fellowships, Honors, and Awards", y, 22)
    awards = [
        "Peter Kennedy Memorial Graduate Fellowship, Simon Fraser University (2026)",
        "Lang Wong Memorial Scholarship in Economics, Simon Fraser University (2025)",
        "FASS Research Travel Award, Simon Fraser University (2025)",
        "PhD Research Scholarship, Simon Fraser University (2023–2025)",
        "Supplemental Graduate Fellowship, Simon Fraser University (2025)",
        "Special Graduate Entrance Scholarship, Simon Fraser University (2024)",
    ]
    for award in awards:
        y = line(pdf, "•  " + award, y, 7) - 5
    y = section(pdf, "Skills", y, 22)
    y = line(pdf, "Languages: Mandarin (native), English (fluent). "
             "Software: R, Stata, Python, LaTeX.", y - 4)
    if y < BOTTOM + 5:
        raise RuntimeError(f"CV page 3 overflow: y={y:.1f}")
    footer(pdf, 3)
    pdf.save()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    build(parser.parse_args().output)
