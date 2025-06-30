from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
import json


def load_data():
    with open("market_analysis.txt", "r") as f:
        market_analysis = f.read()

    with open("gto_recommendations.json", "r") as f:
        gto_recommendations = json.load(f)

    with open("mock_properties.json", "r") as f:
        properties = json.load(f)

    return market_analysis, gto_recommendations, properties


def create_pdf(filename="GTO_Report.pdf"):
    market_analysis, gto_recommendations, properties = load_data()
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Heading", fontSize=16, spaceAfter=12, leading=20))
    styles.add(ParagraphStyle(name="SubHeading", fontSize=12, spaceAfter=10, leading=16))

    doc = SimpleDocTemplate(filename, pagesize=LETTER)
    content = []

    # Title
    content.append(Paragraph("GTO Real Estate Investment Report", styles["Heading"]))
    content.append(Spacer(1, 12))

    # Executive Summary
    content.append(Paragraph("Executive Summary", styles["SubHeading"]))
    content.append(Paragraph("This report provides a Game Theory Optimal (GTO) analysis of NYC commercial properties...", styles["BodyText"]))
    content.append(Spacer(1, 12))

    # Market Intelligence
    content.append(Paragraph("Market Intelligence Analysis", styles["SubHeading"]))
    content.append(Paragraph(market_analysis.replace("\n", "<br/>"), styles["BodyText"]))
    content.append(PageBreak())

    # GTO Recommendations
    content.append(Paragraph("GTO Recommendations", styles["SubHeading"]))
    table_data = [["Property ID", "Score", "Recommendation", "Rationale"]]
    for rec in gto_recommendations:
        table_data.append([
            rec.get("property_id", "N/A"),
            rec.get("gto_score", "N/A"),
            rec.get("recommendation", "N/A"),
            rec.get("rationale", "")[:100] + "..."
        ])
    table = Table(table_data, colWidths=[100, 50, 80, 250])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (1, 1), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    content.append(table)
    content.append(PageBreak())

    # Raw Property Snapshot
    content.append(Paragraph("Raw Property Data (Top 5)", styles["SubHeading"]))
    for prop in properties[:5]:
        prop_text = f"<b>Address:</b> {prop['address']}<br/><b>SqFt:</b> {prop['square_footage']}<br/><b>Price/SF:</b> ${prop['price_per_sqft']}<br/><b>Sale Price:</b> ${prop['sale_price']:,}<br/><b>Cap Rate:</b> {prop['cap_rate']}%<br/><br/>"
        content.append(Paragraph(prop_text, styles["BodyText"]))
        content.append(Spacer(1, 10))

    # Custom Forecast Section
    content.append(PageBreak())
    content.append(Paragraph("Strategic Forecast Notes", styles["SubHeading"]))
    content.append(Paragraph("Add your own notes here based on future outlook, assumptions, or team discussion.", styles["BodyText"]))

    doc.build(content)
    print("✅ PDF report generated as GTO_Report.pdf")


if __name__ == "__main__":
    create_pdf()
