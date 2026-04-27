"""Minimal PDF receipt for a fault report (reportlab)."""

from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def build_fault_pdf(fault) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title=f"CityMenderSA — {fault.tracking_code}",
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "T",
        parent=styles["Heading1"],
        textColor=colors.HexColor("#14532d"),
        spaceAfter=12,
    )
    body = ParagraphStyle(
        "B",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
    )

    story = []
    story.append(Paragraph("CityMenderSA — fault receipt", title_style))
    story.append(
        Paragraph(
            "Keep this document or your tracking code to check progress.",
            body,
        )
    )
    story.append(Spacer(1, 0.4 * cm))

    data = [
        ["Tracking code", fault.tracking_code],
        ["Status", fault.get_status_display()],
        ["Issue", fault.get_issue_type_display()],
        ["Safety fast-track", "Yes" if fault.is_hazard else "No"],
        ["Latitude", f"{fault.latitude:.6f}"],
        ["Longitude", f"{fault.longitude:.6f}"],
        ["Submitted (UTC)", fault.created_at.strftime("%Y-%m-%d %H:%M")],
    ]
    t = Table(data, colWidths=[5 * cm, 10 * cm])
    t.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
            ]
        )
    )
    story.append(t)
    story.append(Spacer(1, 0.6 * cm))
    story.append(Paragraph("<b>Description</b>", body))
    desc = (fault.description or "").replace("\n", "<br/>")
    story.append(Paragraph(desc or "—", body))

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
