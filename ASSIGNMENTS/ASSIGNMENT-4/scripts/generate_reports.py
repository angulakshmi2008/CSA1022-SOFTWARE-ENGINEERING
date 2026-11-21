"""
Report Generator Script: Produces the final academic engineering report for Assignment 4 (CO4).
Outputs:
- docs/submission/Assignment4_Final_Report.docx
- docs/submission/Assignment4_Final_Report.pdf
"""

import os
import sys
from datetime import datetime, timezone
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SUBMISSION_DIR = os.path.join(PROJECT_DIR, "docs", "submission")
os.makedirs(SUBMISSION_DIR, exist_ok=True)

DOCX_OUT = os.path.join(SUBMISSION_DIR, "Assignment4_Final_Report.docx")
PDF_OUT = os.path.join(SUBMISSION_DIR, "Assignment4_Final_Report.pdf")


def set_cell_background(cell, color_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)


def style_table(table, col_widths=None):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(table.rows):
        is_header = (i == 0)
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        if is_header:
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

        for j, cell in enumerate(row.cells):
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
            if col_widths and j < len(col_widths):
                cell.width = Inches(col_widths[j])
            if is_header:
                set_cell_background(cell, "1F497D")  # Deep academic blue
                for p in cell.paragraphs:
                    p.paragraph_format.space_before = Pt(3)
                    p.paragraph_format.space_after = Pt(3)
                    for r in p.runs:
                        r.font.name = "Times New Roman"
                        r.font.size = Pt(10.5)
                        r.font.bold = True
                        r.font.color.rgb = RGBColor(255, 255, 255)
            else:
                bg = "F2F5F8" if i % 2 == 1 else "FFFFFF"
                set_cell_background(cell, bg)
                for p in cell.paragraphs:
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.space_after = Pt(2)
                    for r in p.runs:
                        r.font.name = "Times New Roman"
                        r.font.size = Pt(10)
                        r.font.color.rgb = RGBColor(40, 40, 40)


def add_callout(doc, text, alert_type="NOTE"):
    colors = {
        "NOTE": ("1F497D", "F0F4F8"),
        "IMPORTANT": ("C00000", "FDF2F2"),
        "TIP": ("2E75B6", "F2F7FA"),
        "SECURITY": ("7030A0", "F8F4FA")
    }
    border_col, bg_col = colors.get(alert_type, ("1F497D", "F0F4F8"))
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_col)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=160)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    r_hdr = p.add_run(f"[{alert_type}] ")
    r_hdr.font.name = "Times New Roman"
    r_hdr.font.bold = True
    r_hdr.font.size = Pt(10.5)
    r_hdr.font.color.rgb = RGBColor(31, 73, 125) if alert_type != "IMPORTANT" else RGBColor(192, 0, 0)
    
    r_txt = p.add_run(text)
    r_txt.font.name = "Times New Roman"
    r_txt.font.size = Pt(10)
    r_txt.font.color.rgb = RGBColor(50, 50, 50)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)


def add_code_block(doc, code_str, title=None):
    if title:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(6)
        p_t.paragraph_format.space_after = Pt(2)
        r = p_t.add_run(f"Listing: {title}")
        r.font.name = "Times New Roman"
        r.font.italic = True
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(80, 80, 80)

    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F8F9FA")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=160)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05
    r_code = p.add_run(code_str.strip())
    r_code.font.name = "Consolas"
    r_code.font.size = Pt(9)
    r_code.font.color.rgb = RGBColor(30, 30, 30)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)


print("[*] Report generator library initialized.")
