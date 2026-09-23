"""Génération d'un certificat de traçabilité PDF via ReportLab."""
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from src.domain.services.certificate_generator import (
    CertificateGenerator,
    CertificateInput,
)


class ReportlabCertificateGenerator(CertificateGenerator):
    def generate(self, data: CertificateInput) -> bytes:
        buf = BytesIO()
        doc = SimpleDocTemplate(
            buf, pagesize=A4,
            leftMargin=2*cm, rightMargin=2*cm,
            topMargin=2*cm, bottomMargin=2*cm,
            title=f"Certificat AgriTraceBio {data.lot.lot_code}",
        )
        styles = _styles()
        story = []
        story += _header(styles, data)
        story += _lot_section(styles, data)
        story += _summary_section(styles, data)
        story += _measurements_section(styles, data)
        story += _inspections_section(styles, data)
        story += _blockchain_section(styles, data)
        story += _footer(styles, data)
        doc.build(story)
        return buf.getvalue()


def _styles() -> dict:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "T", parent=base["Title"], fontSize=18, spaceAfter=6,
            textColor=colors.HexColor("#1e5b34")),
        "h2": ParagraphStyle(
            "H2", parent=base["Heading2"], fontSize=13, spaceBefore=14,
            spaceAfter=6, textColor=colors.HexColor("#1e5b34")),
        "body": base["BodyText"],
        "small": ParagraphStyle(
            "S", parent=base["BodyText"], fontSize=8,
            textColor=colors.grey),
    }


def _header(s, d: CertificateInput):
    return [
        Paragraph("AgriTraceBio", s["title"]),
        Paragraph("Certificat de traçabilité — Ananas du Bénin", s["body"]),
        Spacer(1, 6),
        Paragraph(f"Lot n° <b>{d.lot.lot_code}</b>", s["body"]),
        Spacer(1, 12),
    ]


def _lot_section(s, d: CertificateInput):
    lot = d.lot
    rows = [
        ["Producteur", lot.producer_name],
        ["Variété", lot.variety.value.replace("_", " ").title()],
        ["Récolte", lot.harvest_date.strftime("%d/%m/%Y")],
        ["Quantité", f"{lot.quantity_kg:.1f} kg"],
        ["Origine", lot.origin_location],
        ["Destination", lot.destination or "—"],
        ["Statut", lot.status.value],
    ]
    return [Paragraph("Informations du lot", s["h2"]), _kv_table(rows)]


def _summary_section(s, d: CertificateInput):
    crit = sum(1 for a in d.alerts if a.level.value == "critical")
    rejected = sum(1 for i in d.inspections if i.verdict.value == "rejected")
    rows = [
        ["Mesures enregistrées", str(len(d.measurements))],
        ["Alertes totales", str(len(d.alerts))],
        ["Alertes critiques", str(crit)],
        ["Inspections IA", str(len(d.inspections))],
        ["Inspections rejetées", str(rejected)],
        ["Blocs blockchain", str(len(d.blockchain))],
    ]
    return [Paragraph("Résumé qualité", s["h2"]), _kv_table(rows)]


def _measurements_section(s, d: CertificateInput):
    if not d.measurements:
        return [Paragraph("Mesures IoT (dernières 10)", s["h2"]),
                Paragraph("Aucune mesure enregistrée.", s["body"])]
    header = ["Date/heure", "Temp (°C)", "Éthanol", "Air", "Device"]
    rows = [header]
    for m in d.measurements[:10]:
        rows.append([
            m.timestamp.strftime("%d/%m %H:%M"),
            f"{m.temperature:.1f}",
            f"{m.ethanol_ppm:.0f}",
            f"{m.air_quality_ppm:.0f}",
            m.device_id,
        ])
    return [Paragraph("Mesures IoT (dernières 10)", s["h2"]), _data_table(rows)]


def _inspections_section(s, d: CertificateInput):
    if not d.inspections:
        return [Paragraph("Inspections vision par ordinateur", s["h2"]),
                Paragraph("Aucune inspection enregistrée.", s["body"])]
    rows = [["Date/heure", "Verdict", "Détections", "Modèle"]]
    for i in d.inspections[:10]:
        rows.append([
            i.timestamp.strftime("%d/%m %H:%M"),
            i.verdict.value,
            str(len(i.detections)),
            i.model_version,
        ])
    return [Paragraph("Inspections vision par ordinateur", s["h2"]),
            _data_table(rows)]


def _blockchain_section(s, d: CertificateInput):
    if not d.blockchain:
        return []
    last = d.blockchain[-1]
    para = (f"<b>Preuve blockchain</b> — {len(d.blockchain)} événements chaînés. "
            f"Dernier hash : <font face='Courier'>{last.hash}</font>")
    return [Paragraph("Intégrité", s["h2"]), Paragraph(para, s["body"])]


def _footer(s, d: CertificateInput):
    return [
        Spacer(1, 18),
        Paragraph(
            f"Vérifiez ce lot en scannant le QR code ou via : "
            f"<font face='Courier'>{d.trace_url}</font>",
            s["small"],
        ),
    ]


def _kv_table(rows: list[list[str]]) -> Table:
    t = Table(rows, colWidths=[5*cm, 11*cm])
    t.setStyle(TableStyle([
        ("FONT", (0, 0), (0, -1), "Helvetica-Bold"),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f2f7ea")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def _data_table(rows: list[list[str]]) -> Table:
    t = Table(rows, repeatRows=1)
    t.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e5b34")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#f7faf3")]),
    ]))
    return t
