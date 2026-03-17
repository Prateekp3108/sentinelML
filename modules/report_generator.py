import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT


# ── Colour palette matching the site ─────────────────────────────────────
BG         = colors.HexColor("#F7F6F0")
BLACK      = colors.HexColor("#0a0a0a")
GREY_DARK  = colors.HexColor("#444444")
GREY_MID   = colors.HexColor("#888888")
GREY_LIGHT = colors.HexColor("#cccccc")
RED        = colors.HexColor("#c0392b")
GREEN      = colors.HexColor("#276749")
AMBER      = colors.HexColor("#b7791f")
RED_BG     = colors.HexColor("#fef0ef")
GREEN_BG   = colors.HexColor("#f0fff4")
AMBER_BG   = colors.HexColor("#fffbeb")
WHITE      = colors.white


def generate_report(model_result, attack_results=None, trojan_results=None):
    """
    Generates a PDF security audit report and returns it as bytes.

    Arguments:
        model_result   -- dict from modules/model_loader.py
        attack_results -- dict from modules/adversarial.py  (optional)
        trojan_results -- dict from modules/trojan_detector.py (optional)

    Returns:
        bytes — the PDF file content, ready for st.download_button()
    """

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    story = []

    # ── STYLES ────────────────────────────────────────────────────────────
    def style(name, **kwargs):
        defaults = dict(fontName="Helvetica", fontSize=10,
                        textColor=BLACK, leading=14, spaceAfter=0)
        defaults.update(kwargs)
        return ParagraphStyle(name, **defaults)

    s_eyebrow   = style("eyebrow",  fontSize=7,  textColor=GREY_LIGHT,
                        fontName="Helvetica", leading=10, spaceAfter=4,
                        letterSpacing=2)
    s_title     = style("title",    fontSize=26, fontName="Helvetica-Bold",
                        leading=30, spaceAfter=4)
    s_subtitle  = style("subtitle", fontSize=10, textColor=GREY_MID,
                        leading=14, spaceAfter=0)
    s_h2        = style("h2",       fontSize=13, fontName="Helvetica-Bold",
                        leading=18, spaceAfter=6)
    s_h3        = style("h3",       fontSize=9,  textColor=GREY_LIGHT,
                        fontName="Helvetica", leading=12, spaceAfter=4,
                        letterSpacing=1.5)
    s_body      = style("body",     fontSize=9,  textColor=GREY_DARK,
                        leading=14, spaceAfter=0)
    s_mono      = style("mono",     fontSize=8,  fontName="Courier",
                        textColor=GREY_DARK, leading=12, spaceAfter=0)
    s_badge_r   = style("badge_r",  fontSize=8,  fontName="Helvetica-Bold",
                        textColor=RED,   leading=11)
    s_badge_g   = style("badge_g",  fontSize=8,  fontName="Helvetica-Bold",
                        textColor=GREEN, leading=11)
    s_badge_a   = style("badge_a",  fontSize=8,  fontName="Helvetica-Bold",
                        textColor=AMBER, leading=11)
    s_score     = style("score",    fontSize=52, fontName="Helvetica-Bold",
                        leading=56, spaceAfter=0)
    s_right     = style("right",    fontSize=8,  textColor=GREY_MID,
                        alignment=TA_RIGHT, leading=11)

    def divider(color=GREY_LIGHT, thickness=0.5, space=8):
        return [
            Spacer(1, space),
            HRFlowable(width="100%", thickness=thickness,
                       color=color, spaceAfter=space),
        ]

    # ── HEADER ────────────────────────────────────────────────────────────
    generated_at = datetime.now().strftime("%B %d, %Y — %H:%M UTC")

    story.append(Spacer(1, 4))
    story.append(Paragraph("SENTINEL(ML)", s_eyebrow))
    story.append(Paragraph("Security Audit Report", s_title))
    story.append(Paragraph(f"Generated {generated_at}", s_subtitle))
    story += divider(thickness=1, space=12)

    # ── MODEL OVERVIEW ────────────────────────────────────────────────────
    story.append(Paragraph("MODEL OVERVIEW", s_h3))
    story.append(Spacer(1, 4))

    from modules.model_loader import format_param_count

    overview_data = [
        ["Parameter", "Value"],
        ["Total Parameters",   format_param_count(model_result.get("total_params", 0))],
        ["Trainable Params",   format_param_count(model_result.get("trainable_params", 0))],
        ["Total Layers",       str(model_result.get("num_layers", "?"))],
        ["Output Classes",     str(model_result.get("num_classes", "?"))],
        ["Input Size",         f'{model_result.get("input_size", "?")}px'
                               if model_result.get("input_size") else "?"],
    ]

    overview_table = Table(overview_data, colWidths=[2.8 * inch, 4.2 * inch])
    overview_table.setStyle(TableStyle([
        # Header row
        ("BACKGROUND",   (0, 0), (-1, 0), BLACK),
        ("TEXTCOLOR",    (0, 0), (-1, 0), WHITE),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, 0), 8),
        ("TOPPADDING",   (0, 0), (-1, 0), 7),
        ("BOTTOMPADDING",(0, 0), (-1, 0), 7),
        ("LEFTPADDING",  (0, 0), (-1, 0), 10),
        # Data rows
        ("FONTNAME",     (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",     (0, 1), (-1, -1), 9),
        ("TEXTCOLOR",    (0, 1), (0, -1),  GREY_MID),
        ("TEXTCOLOR",    (1, 1), (1, -1),  BLACK),
        ("TOPPADDING",   (0, 1), (-1, -1), 7),
        ("BOTTOMPADDING",(0, 1), (-1, -1), 7),
        ("LEFTPADDING",  (0, 1), (-1, -1), 10),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, colors.HexColor("#fafafa")]),
        ("LINEBELOW",    (0, 0), (-1, -1), 0.5, colors.HexColor("#eeeeee")),
        ("BOX",          (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
        ("ROUNDEDCORNERS", [4]),
    ]))

    story.append(overview_table)

    # Layer list
    layer_names = model_result.get("layer_names", [])
    if layer_names:
        story.append(Spacer(1, 14))
        story.append(Paragraph("LAYER ARCHITECTURE", s_h3))
        story.append(Spacer(1, 4))

        # Show up to 30 layers, truncate with note if more
        display_layers = layer_names[:30]
        truncated      = len(layer_names) > 30

        layer_rows = [["#", "Layer Name"]]
        for i, name in enumerate(display_layers):
            layer_rows.append([f"{i+1:02d}", name])

        if truncated:
            layer_rows.append(["...", f"+ {len(layer_names) - 30} more layers"])

        layer_table = Table(layer_rows, colWidths=[0.4 * inch, 6.6 * inch])
        layer_table.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, 0), BLACK),
            ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
            ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE",      (0, 0), (-1, 0), 8),
            ("TOPPADDING",    (0, 0), (-1, 0), 6),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
            ("LEFTPADDING",   (0, 0), (-1, 0), 8),
            ("FONTNAME",      (0, 1), (-1, -1), "Courier"),
            ("FONTSIZE",      (0, 1), (-1, -1), 7.5),
            ("TEXTCOLOR",     (0, 1), (0, -1),  GREY_LIGHT),
            ("TEXTCOLOR",     (1, 1), (1, -1),  GREY_DARK),
            ("TOPPADDING",    (0, 1), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 5),
            ("LEFTPADDING",   (0, 1), (-1, -1), 8),
            ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, colors.HexColor("#fafafa")]),
            ("LINEBELOW",     (0, 0), (-1, -1), 0.3, colors.HexColor("#eeeeee")),
            ("BOX",           (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
        ]))
        story.append(layer_table)

    # ── ADVERSARIAL RESULTS ───────────────────────────────────────────────
    if attack_results:
        story += divider(space=16)
        story.append(Paragraph("ADVERSARIAL ATTACK RESULTS", s_h3))
        story.append(Spacer(1, 6))

        score       = attack_results.get("robustness_score", 0)
        score_color = GREEN if score >= 70 else AMBER if score >= 40 else RED
        score_label = "ROBUST" if score >= 70 else "MODERATE" if score >= 40 else "VULNERABLE"

        # Score display
        score_table = Table(
            [[Paragraph(str(score), ParagraphStyle("sc", fontName="Helvetica-Bold",
              fontSize=48, textColor=score_color, leading=52)),
              Paragraph(f"/ 100\n{score_label}\nRobustness Score",
              ParagraphStyle("sl", fontName="Helvetica", fontSize=9,
              textColor=GREY_MID, leading=14))]],
            colWidths=[1.2 * inch, 5.8 * inch]
        )
        score_table.setStyle(TableStyle([
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING",   (0, 0), (-1, -1), 16),
            ("TOPPADDING",    (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ("BACKGROUND",    (0, 0), (-1, -1), colors.HexColor("#fafafa")),
            ("BOX",           (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
            ("ROUNDEDCORNERS", [4]),
        ]))
        story.append(score_table)
        story.append(Spacer(1, 12))

        # Attack rows
        attack_meta = {
            "fgsm":     ("FGSM",     "Fast Gradient Sign Method — one-step attack"),
            "bim":      ("BIM",      "Basic Iterative Method — 10 iterations"),
            "deepfool": ("DeepFool", "Minimum perturbation — strongest attack"),
        }

        atk_rows = [["Attack", "Description", "Result"]]
        for key, (name, desc) in attack_meta.items():
            r = attack_results.get(key, {})
            if "error" in r:
                result_str = "Error"
                result_col = AMBER
            elif r.get("success"):
                orig = r.get("original_conf", "?")
                adv  = r.get("adversarial_conf", "?")
                result_str = f"Fooled ({orig}% -> {adv}%)"
                result_col = RED
            else:
                result_str = "Resisted"
                result_col = GREEN

            atk_rows.append([
                Paragraph(name, ParagraphStyle("an", fontName="Courier",
                          fontSize=8, textColor=BLACK, leading=11)),
                Paragraph(desc, ParagraphStyle("ad", fontName="Helvetica",
                          fontSize=8, textColor=GREY_MID, leading=11)),
                Paragraph(result_str, ParagraphStyle("ar", fontName="Helvetica-Bold",
                          fontSize=8, textColor=result_col, leading=11)),
            ])

        atk_table = Table(atk_rows, colWidths=[1.2*inch, 3.8*inch, 2.0*inch])
        atk_table.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, 0), BLACK),
            ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
            ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE",      (0, 0), (-1, 0), 8),
            ("TOPPADDING",    (0, 0), (-1, 0), 7),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 7),
            ("LEFTPADDING",   (0, 0), (-1, 0), 10),
            ("TOPPADDING",    (0, 1), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
            ("LEFTPADDING",   (0, 1), (-1, -1), 10),
            ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, colors.HexColor("#fafafa")]),
            ("LINEBELOW",     (0, 0), (-1, -1), 0.3, colors.HexColor("#eeeeee")),
            ("BOX",           (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ]))
        story.append(atk_table)

    # ── TROJAN RESULTS ────────────────────────────────────────────────────
    if trojan_results and not trojan_results.get("error"):
        story += divider(space=16)
        story.append(Paragraph("TROJAN / BACKDOOR DETECTION", s_h3))
        story.append(Spacer(1, 6))

        detected      = trojan_results.get("trojan_detected", False)
        anomaly_index = trojan_results.get("anomaly_index", 0)
        confidence    = trojan_results.get("confidence", "N/A")
        suspect_class = trojan_results.get("suspected_target_class")
        classes_scanned = trojan_results.get("classes_scanned", 0)

        verdict_color = RED if detected else GREEN
        verdict_text  = "TROJAN DETECTED" if detected else "NO TROJAN FOUND"
        verdict_sub   = (
            f"Confidence: {confidence} | Suspected target class: {suspect_class}"
            if detected else
            "No suspicious backdoor triggers found across scanned classes"
        )

        verdict_table = Table(
            [[Paragraph(verdict_text,
               ParagraphStyle("vt", fontName="Helvetica-Bold",
               fontSize=14, textColor=verdict_color, leading=18)),
              Paragraph(f"Anomaly Index: {anomaly_index}",
               ParagraphStyle("vi", fontName="Courier",
               fontSize=9, textColor=verdict_color, leading=12,
               alignment=TA_RIGHT))]],
            colWidths=[4.5*inch, 2.5*inch]
        )
        verdict_table.setStyle(TableStyle([
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING",   (0, 0), (-1, -1), 14),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 14),
            ("TOPPADDING",    (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ("BACKGROUND",    (0, 0), (-1, -1),
             RED_BG if detected else GREEN_BG),
            ("BOX",           (0, 0), (-1, -1), 0.5,
             RED if detected else GREEN),
            ("ROUNDEDCORNERS", [4]),
        ]))
        story.append(verdict_table)
        story.append(Spacer(1, 6))
        story.append(Paragraph(verdict_sub, s_body))
        story.append(Spacer(1, 12))

        # Trigger norm table
        norms = trojan_results.get("trigger_norms", [])
        if norms:
            story.append(Paragraph("TRIGGER NORM PER CLASS", s_h3))
            story.append(Spacer(1, 4))
            story.append(Paragraph(
                "Smaller norm = smaller trigger needed = more suspicious",
                s_body))
            story.append(Spacer(1, 6))

            norm_rows = [["Class", "Trigger Norm", "Flag"]]
            for i, n in enumerate(norms):
                is_suspect = detected and i == suspect_class
                flag = "SUSPECTED BACKDOOR TARGET" if is_suspect else ""
                norm_rows.append([
                    Paragraph(f"Class {i:02d}",
                      ParagraphStyle("nc", fontName="Courier",
                      fontSize=8, textColor=RED if is_suspect else GREY_DARK,
                      leading=11)),
                   Paragraph(f"{n:.4f}",
                      ParagraphStyle("nv",
                      fontName="Courier-Bold" if is_suspect else "Courier",
                      fontSize=8, textColor=RED if is_suspect else BLACK,
                      leading=11)),
                    Paragraph(flag,
                      ParagraphStyle("nf", fontName="Helvetica-Bold",
                      fontSize=7, textColor=RED, leading=10)),
                ])

            norm_table = Table(norm_rows,
                               colWidths=[1.2*inch, 1.8*inch, 4.0*inch])
            norm_table.setStyle(TableStyle([
                ("BACKGROUND",    (0, 0), (-1, 0), BLACK),
                ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
                ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE",      (0, 0), (-1, 0), 8),
                ("TOPPADDING",    (0, 0), (-1, 0), 7),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 7),
                ("LEFTPADDING",   (0, 0), (-1, 0), 10),
                ("TOPPADDING",    (0, 1), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
                ("LEFTPADDING",   (0, 1), (-1, -1), 10),
                ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, colors.HexColor("#fafafa")]),
                ("LINEBELOW",     (0, 0), (-1, -1), 0.3, colors.HexColor("#eeeeee")),
                ("BOX",           (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
                ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
            ]))
            story.append(norm_table)

        # Detection metadata
        story.append(Spacer(1, 12))
        meta_rows = [
            ["Detection method",  "Neural Cleanse (MAD anomaly scoring)"],
            ["Classes scanned",   str(classes_scanned)],
            ["Anomaly threshold", "2.0"],
            ["Optimisation steps","100 per class"],
        ]
        meta_table = Table(meta_rows, colWidths=[2.0*inch, 5.0*inch])
        meta_table.setStyle(TableStyle([
            ("FONTNAME",      (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE",      (0, 0), (-1, -1), 8),
            ("TEXTCOLOR",     (0, 0), (0, -1),  GREY_MID),
            ("TEXTCOLOR",     (1, 0), (1, -1),  BLACK),
            ("TOPPADDING",    (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING",   (0, 0), (-1, -1), 10),
            ("ROWBACKGROUNDS",(0, 0), (-1, -1), [WHITE, colors.HexColor("#fafafa")]),
            ("LINEBELOW",     (0, 0), (-1, -1), 0.3, colors.HexColor("#eeeeee")),
            ("BOX",           (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
        ]))
        story.append(meta_table)

    # ── FOOTER ────────────────────────────────────────────────────────────
    story += divider(space=16)
    story.append(Paragraph(
        "Generated by SentinelML — ML Model Security Auditor",
        ParagraphStyle("footer", fontName="Helvetica", fontSize=7,
                       textColor=GREY_LIGHT, leading=10, alignment=TA_CENTER)
    ))
    story.append(Paragraph(
        "This report is for security research purposes only.",
        ParagraphStyle("footer2", fontName="Helvetica", fontSize=7,
                       textColor=GREY_LIGHT, leading=10, alignment=TA_CENTER)
    ))

    # ── BUILD ─────────────────────────────────────────────────────────────
    doc.build(story)
    buffer.seek(0)
    return buffer.read()