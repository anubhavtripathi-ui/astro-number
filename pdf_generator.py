from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from io import BytesIO

def generate_pdf(name, dob, mulank, bhagyank, personal_year, missing, count, personality, enemy):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    normal_style = styles["Normal"]

    elements.append(Paragraph("Astro-Number Professional Report", title_style))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph(f"Name: {name}", normal_style))
    elements.append(Paragraph(f"DOB: {dob}", normal_style))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph(f"Mulank: {mulank}", normal_style))
    elements.append(Paragraph(f"Bhagyank: {bhagyank}", normal_style))
    elements.append(Paragraph(f"Personal Year: {personal_year}", normal_style))
    elements.append(Paragraph(f"Enemy Number: {enemy}", normal_style))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph(f"Missing Numbers: {', '.join(map(str, missing))}", normal_style))
    elements.append(Spacer(1, 0.2 * inch))

    strength_text = ", ".join([f"{num} ({freq})" for num, freq in count.items()])
    elements.append(Paragraph(f"Strength Meter: {strength_text}", normal_style))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph("Personality Insight:", styles["Heading2"]))
    elements.append(Paragraph(personality, normal_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer
