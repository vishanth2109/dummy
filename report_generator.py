from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from io import BytesIO


def generate_pdf(score, ai_result, matched_skills, missing_skills):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    elements = []

    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]
    heading_style = styles["Heading1"]

    # Title
    elements.append(Paragraph("AI Resume Analysis Report", heading_style))
    elements.append(Spacer(1, 0.3 * inch))

    # ATS Score
    elements.append(Paragraph(f"<b>ATS Score:</b> {score}%", normal_style))
    elements.append(Spacer(1, 0.3 * inch))

    # Matched Skills
    elements.append(Paragraph("<b>Matched Skills:</b>", normal_style))
    elements.append(Spacer(1, 0.2 * inch))

    matched_list = [ListItem(Paragraph(skill, normal_style)) for skill in matched_skills]
    elements.append(ListFlowable(matched_list, bulletType="bullet"))
    elements.append(Spacer(1, 0.3 * inch))

    # Missing Skills
    elements.append(Paragraph("<b>Missing Skills:</b>", normal_style))
    elements.append(Spacer(1, 0.2 * inch))

    missing_list = [ListItem(Paragraph(skill, normal_style)) for skill in missing_skills]
    elements.append(ListFlowable(missing_list, bulletType="bullet"))
    elements.append(Spacer(1, 0.3 * inch))

    # AI Analysis
    elements.append(Paragraph("<b>AI Detailed Analysis:</b>", normal_style))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph(ai_result.replace("\n", "<br/>"), normal_style))

    doc.build(elements)

    buffer.seek(0)
    return buffer