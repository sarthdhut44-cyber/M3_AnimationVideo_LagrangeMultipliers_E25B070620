"""Generate Storyboard.pdf and Narration_Script.md from script_data.py."""

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from script_data import (
    BATCH,
    BEATS,
    CONCEPT,
    COURSE,
    LAB_BATCH,
    LEARNING_OBJECTIVE,
    SCENE_PLAN,
    STUDENT_NAME,
    STUDENT_URN,
    VIDEO_TITLE,
)


def build_storyboard_pdf(out_pdf: str) -> None:
    doc = SimpleDocTemplate(
        out_pdf,
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
    )
    styles = getSampleStyleSheet()
    navy = colors.HexColor("#0F294A")
    slate = colors.HexColor("#334155")
    accent = colors.HexColor("#0284C7")
    bg_light = colors.HexColor("#F1F5F9")

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=17,
        leading=21,
        textColor=navy,
        spaceAfter=4,
    )
    subtitle_style = ParagraphStyle(
        "DocSub",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=13,
        textColor=accent,
        spaceAfter=8,
    )
    h2_style = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=navy,
        spaceBefore=10,
        spaceAfter=5,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.2,
        leading=13,
        textColor=slate,
    )
    cell_style = ParagraphStyle(
        "Cell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=slate,
    )
    cell_bold = ParagraphStyle(
        "CellBold",
        parent=cell_style,
        fontName="Helvetica-Bold",
        textColor=navy,
    )

    story = []
    story.append(Paragraph(COURSE.upper(), subtitle_style))
    story.append(Paragraph("6-Scene Animation Storyboard: Lagrange Multipliers", title_style))
    story.append(Spacer(1, 3 * mm))

    meta_rows = [
        [Paragraph("<b>Student Name</b>", cell_bold), Paragraph(STUDENT_NAME, cell_style),
         Paragraph("<b>URN / Student ID</b>", cell_bold), Paragraph(STUDENT_URN, cell_style)],
        [Paragraph("<b>Batch / Lab</b>", cell_bold), Paragraph(f"{BATCH} / {LAB_BATCH}", cell_style),
         Paragraph("<b>Selected Concept</b>", cell_bold), Paragraph(CONCEPT, cell_style)],
        [Paragraph("<b>Video Title</b>", cell_bold), Paragraph(VIDEO_TITLE, cell_style),
         Paragraph("<b>Target Format</b>", cell_bold), Paragraph("1920x1080 (16:9), MP4, ~5-6 min", cell_style)],
    ]
    meta_table = Table(meta_rows, colWidths=[30 * mm, 60 * mm, 32 * mm, 56 * mm])
    meta_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), bg_light),
            ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#CBD5E1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ])
    )
    story.append(meta_table)
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("One-Sentence Learning Objective", h2_style))
    obj_table = Table(
        [[Paragraph(f"<i>{LEARNING_OBJECTIVE}</i>", body_style)]],
        colWidths=[178 * mm],
    )
    obj_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#E0F2FE")),
            ("LINEBEFORE", (0, 0), (0, -1), 3, accent),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LEFTPADDING", (0, 0), (-1, -1), 9),
            ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ])
    )
    story.append(obj_table)
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("6-Scene Storyboard Plan", h2_style))

    narration_by_scene = {}
    for b in BEATS:
        narration_by_scene.setdefault(b.scene_num, []).append(b.narration)

    table_data = [[
        Paragraph("<b>Scene</b>", ParagraphStyle("TH", parent=cell_bold, textColor=colors.white)),
        Paragraph("<b>Purpose</b>", ParagraphStyle("TH", parent=cell_bold, textColor=colors.white)),
        Paragraph("<b>Visual, Narration & Math Plan</b>", ParagraphStyle("TH", parent=cell_bold, textColor=colors.white)),
    ]]

    for idx, item in enumerate(SCENE_PLAN, start=1):
        narr_summary = " ".join(narration_by_scene.get(idx, []))
        if len(narr_summary) > 360:
            narr_summary = narr_summary[:357].rsplit(" ", 1)[0] + "..."
        plan_html = (
            f"<b>Visuals:</b> {item['visual']}<br/>"
            f"<b>Mathematics:</b> {item['math']}<br/>"
            f"<b>Narration Cue:</b> <i>\"{narr_summary}\"</i>"
        )
        table_data.append([
            Paragraph(item["scene"], cell_bold),
            Paragraph(item["purpose"], cell_style),
            Paragraph(plan_html, cell_style),
        ])

    sb_table = Table(table_data, colWidths=[30 * mm, 36 * mm, 112 * mm], repeatRows=1)
    sb_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), navy),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
            ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#CBD5E1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ])
    )
    story.append(sb_table)
    story.append(Spacer(1, 5 * mm))

    story.append(Paragraph("Mathematical Verification & AI Tool Disclosure Summary", h2_style))
    story.append(
        Paragraph(
            "• <b>Worked Example:</b> Maximize/minimize f(x, y) = xy subject to g(x, y) = x^2 + y^2 - 8 = 0. "
            "Gradients: grad f = (y, x), grad g = (2x, 2y). Regularity holds since grad g = (0,0) only at (0,0), "
            "which does not lie on the circle. Solving grad f = lambda grad g yields y = 2 lambda x and x = 2 lambda y, "
            "with x, y != 0 (otherwise x=y=0 violates x^2+y^2=8). Thus y^2 = x^2 => y = +-x, giving four extrema on the compact circle: "
            "maxima f(2,2) = f(-2,-2) = +4 (lambda = +1/2) and minima f(2,-2) = f(-2,2) = -4 (lambda = -1/2).<br/>"
            "• <b>Tools & AI Disclosure:</b> Animation rendered programmatically in Python (Matplotlib, NumPy, SciPy, Pillow, FFmpeg). "
            "Neural voice-over generated via Microsoft Edge TTS (edge-tts); AI coding/scripting assistance used for storyboard drafting, "
            "Python animation architecture, and narration timing.",
            body_style,
        )
    )

    doc.build(story)


def build_narration_md(out_md: str) -> None:
    lines = [
        f"# Narration Script — {VIDEO_TITLE}",
        "",
        f"- **Student:** {STUDENT_NAME} (`{STUDENT_URN}`)",
        f"- **Batch / Lab Batch:** {BATCH} / {LAB_BATCH}",
        f"- **Learning Objective:** {LEARNING_OBJECTIVE}",
        "",
    ]
    current_scene = None
    word_count = 0
    for b in BEATS:
        if b.scene_num != current_scene:
            current_scene = b.scene_num
            lines.append(f"## Scene {b.scene_name}")
            lines.append("")
        lines.append(f"### `{b.beat_id}` (pause after: {b.post_pause_sec:.2f}s)")
        lines.append(b.narration)
        lines.append("")
        word_count += len(b.narration.split())

    lines.insert(5, f"- **Total Spoken Words:** {word_count}")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main() -> None:
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_pdf = os.path.join(repo_root, "Storyboard.pdf")
    out_md = os.path.join(repo_root, "Narration_Script.md")
    build_storyboard_pdf(out_pdf)
    build_narration_md(out_md)
    print(f"Generated {out_pdf} and {out_md}")


if __name__ == "__main__":
    main()
