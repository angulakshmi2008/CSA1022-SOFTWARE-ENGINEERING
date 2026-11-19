"""
Experiment 10: MoSCoW Prioritization of Library Management System Requirements
Student: Angulakshmi S (Reg No: 192524402)
Course: CSA10 - Software Engineering
Course Outcome: CO2

This script generates:
1. A professionally formatted Excel file 'Library_Management_System_MoSCoW.xlsx'
   with color-coded MoSCoW categories, formula-based summaries, and an embedded native Excel chart.
2. A high-resolution chart image 'output/moscow_distribution_chart.png' via matplotlib.
"""

import os
import csv
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference
import matplotlib.pyplot as plt

def generate_excel_and_charts():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "Library_Management_System_MoSCoW.csv")
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    excel_out_path = os.path.join(output_dir, "Library_Management_System_MoSCoW.xlsx")
    chart_out_path = os.path.join(output_dir, "moscow_distribution_chart.png")

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "MoSCoW Analysis"
    ws.views.sheetView[0].showGridLines = True

    # Styling elements
    font_title = Font(name="Calibri", size=14, bold=True, color="1F497D")
    font_sub = Font(name="Calibri", size=10, italic=True, color="595959")
    font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    font_data = Font(name="Calibri", size=10)
    font_bold = Font(name="Calibri", size=10, bold=True)

    fill_header = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    fill_summary_hdr = PatternFill(start_color="2F5597", end_color="2F5597", fill_type="solid")

    # Category fills
    fill_must = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    font_must = Font(name="Calibri", size=10, bold=True, color="006100")

    fill_should = PatternFill(start_color="BDD7EE", end_color="BDD7EE", fill_type="solid")
    font_should = Font(name="Calibri", size=10, bold=True, color="1F4E78")

    fill_could = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")
    font_could = Font(name="Calibri", size=10, bold=True, color="9C6500")

    fill_wont = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    font_wont = Font(name="Calibri", size=10, bold=True, color="9C0006")

    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )

    # Title Banner
    ws.merge_cells("A1:F1")
    ws["A1"] = "Saveetha School of Engineering | Department of AI & DS / CSE"
    ws["A1"].font = font_title
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")

    ws.merge_cells("A2:F2")
    ws["A2"] = "CSA10 - Software Engineering | Experiment 10: Library Management System MoSCoW Prioritization"
    ws["A2"].font = font_sub
    ws["A2"].alignment = Alignment(horizontal="center", vertical="center")

    ws.merge_cells("A3:F3")
    ws["A3"] = "Student: Angulakshmi S | Register Number: 192524402 | Date: 19-11-2026"
    ws["A3"].font = font_sub
    ws["A3"].alignment = Alignment(horizontal="center", vertical="center")

    # Table Header at Row 5
    headers = ["Requirement ID", "Requirement Description", "MoSCoW Category", "User Impact", "Feasibility", "Justification"]
    for col_idx, h in enumerate(headers, start=1):
        cell = ws.cell(row=5, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    # Read CSV and populate data
    row_idx = 6
    category_counts = {"Must Have": 0, "Should Have": 0, "Could Have": 0, "Won't Have": 0}

    with open(data_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ws.cell(row=row_idx, column=1, value=row["Requirement ID"]).alignment = Alignment(horizontal="center")
            ws.cell(row=row_idx, column=2, value=row["Requirement Description"]).alignment = Alignment(horizontal="left")
            
            cat_cell = ws.cell(row=row_idx, column=3, value=row["MoSCoW Category"])
            cat_cell.alignment = Alignment(horizontal="center")
            category = row["MoSCoW Category"]
            if category == "Must Have":
                cat_cell.fill = fill_must
                cat_cell.font = font_must
                category_counts["Must Have"] += 1
            elif category == "Should Have":
                cat_cell.fill = fill_should
                cat_cell.font = font_should
                category_counts["Should Have"] += 1
            elif category == "Could Have":
                cat_cell.fill = fill_could
                cat_cell.font = font_could
                category_counts["Could Have"] += 1
            else:
                cat_cell.fill = fill_wont
                cat_cell.font = font_wont
                category_counts["Won't Have"] += 1

            ws.cell(row=row_idx, column=4, value=row["User Impact"]).alignment = Alignment(horizontal="center")
            ws.cell(row=row_idx, column=5, value=row["Implementation Feasibility"]).alignment = Alignment(horizontal="center")
            ws.cell(row=row_idx, column=6, value=row["Justification"]).alignment = Alignment(horizontal="left", wrap_text=True)

            for c in range(1, 7):
                ws.cell(row=row_idx, column=c).border = thin_border
                if c != 3:
                    ws.cell(row=row_idx, column=c).font = font_data
            row_idx += 1

    # Summary Statistics Table
    summary_start_row = row_idx + 2
    ws.cell(row=summary_start_row, column=1, value="MoSCoW Category").fill = fill_summary_hdr
    ws.cell(row=summary_start_row, column=1).font = font_header
    ws.cell(row=summary_start_row, column=1).alignment = Alignment(horizontal="center")

    ws.cell(row=summary_start_row, column=2, value="Requirement Count").fill = fill_summary_hdr
    ws.cell(row=summary_start_row, column=2).font = font_header
    ws.cell(row=summary_start_row, column=2).alignment = Alignment(horizontal="center")

    ws.cell(row=summary_start_row, column=3, value="Percentage (%)").fill = fill_summary_hdr
    ws.cell(row=summary_start_row, column=3).font = font_header
    ws.cell(row=summary_start_row, column=3).alignment = Alignment(horizontal="center")

    s_row = summary_start_row + 1
    categories = [("Must Have", fill_must, font_must),
                  ("Should Have", fill_should, font_should),
                  ("Could Have", fill_could, font_could),
                  ("Won't Have", fill_wont, font_wont)]

    for cat_name, c_fill, c_font in categories:
        ws.cell(row=s_row, column=1, value=cat_name).font = c_font
        ws.cell(row=s_row, column=1).fill = c_fill
        ws.cell(row=s_row, column=1).alignment = Alignment(horizontal="center")
        ws.cell(row=s_row, column=1).border = thin_border

        # Use Excel COUNTIF formula
        count_cell = ws.cell(row=s_row, column=2, value=f'=COUNTIF(C6:C15, "{cat_name}")')
        count_cell.font = font_bold
        count_cell.alignment = Alignment(horizontal="center")
        count_cell.border = thin_border

        pct_cell = ws.cell(row=s_row, column=3, value=f'=(B{s_row}/10)*100')
        pct_cell.font = font_bold
        pct_cell.alignment = Alignment(horizontal="center")
        pct_cell.number_format = '0.0"%"'
        pct_cell.border = thin_border
        s_row += 1

    # Total row
    ws.cell(row=s_row, column=1, value="Total Requirements").font = font_bold
    ws.cell(row=s_row, column=1).alignment = Alignment(horizontal="center")
    ws.cell(row=s_row, column=1).border = thin_border

    tot_count_cell = ws.cell(row=s_row, column=2, value=f'=SUM(B{summary_start_row+1}:B{s_row-1})')
    tot_count_cell.font = font_bold
    tot_count_cell.alignment = Alignment(horizontal="center")
    tot_count_cell.border = thin_border

    tot_pct_cell = ws.cell(row=s_row, column=3, value=f'=SUM(C{summary_start_row+1}:C{s_row-1})')
    tot_pct_cell.font = font_bold
    tot_pct_cell.alignment = Alignment(horizontal="center")
    tot_pct_cell.number_format = '0.0"%"'
    tot_pct_cell.border = thin_border

    # Add embedded Excel Bar Chart
    chart = BarChart()
    chart.type = "col"
    chart.style = 10
    chart.title = "MoSCoW Category Breakdown"
    chart.y_axis.title = "Number of Requirements"
    chart.x_axis.title = "Category"
    chart.legend = None

    data_ref = Reference(ws, min_col=2, min_row=summary_start_row, max_row=s_row-1)
    cats_ref = Reference(ws, min_col=1, min_row=summary_start_row+1, max_row=s_row-1)
    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(cats_ref)
    chart.width = 14
    chart.height = 7
    ws.add_chart(chart, f"D{summary_start_row}")

    # Set column widths
    column_widths = {'A': 16, 'B': 42, 'C': 18, 'D': 14, 'E': 16, 'F': 55}
    for col, width in column_widths.items():
        ws.column_dimensions[col].width = width

    wb.save(excel_out_path)
    print(f"Generated formatted Excel file at: {excel_out_path}")

    # Generate Matplotlib chart image
    fig, ax = plt.subplots(figsize=(7, 5), dpi=300)
    cats = list(category_counts.keys())
    counts = list(category_counts.values())
    colors = ['#27AE60', '#2980B9', '#F39C12', '#E74C3C']

    bars = ax.bar(cats, counts, color=colors, width=0.55, edgecolor='#2C3E50', linewidth=1.2)
    ax.set_title("Library Management System: MoSCoW Requirements Distribution\nSaveetha School of Engineering | Angulakshmi S (192524402)", fontsize=10.5, fontweight='bold', pad=12)
    ax.set_xlabel("MoSCoW Category", fontsize=10, fontweight='bold')
    ax.set_ylabel("Number of Requirements", fontsize=10, fontweight='bold')
    ax.set_ylim(0, 5)
    ax.grid(axis='y', linestyle=':', alpha=0.7)

    for bar in bars:
        h = bar.get_height()
        pct = (h / sum(counts)) * 100
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.15, f"{h} ({pct:.0f}%)",
                ha='center', va='bottom', fontsize=9.5, fontweight='bold')

    plt.tight_layout()
    plt.savefig(chart_out_path, dpi=300)
    plt.close()
    print(f"Generated standalone chart image at: {chart_out_path}")

    # Print summary to stdout
    print("\n==================================================================")
    print("   EXPERIMENT 10: MOSCOW PRIORITIZATION EVALUATION COMPLETE       ")
    print("==================================================================")
    print(f"{'Category':<15} | {'Count':<8} | {'Percentage':<10}")
    print("-" * 40)
    for c, cnt in category_counts.items():
        print(f"{c:<15} | {cnt:<8} | {cnt/10*100:>8.1f}%")
    print("-" * 40)
    print(f"{'Total':<15} | {10:<8} | {100.0:>8.1f}%")
    print("==================================================================")

if __name__ == "__main__":
    generate_excel_and_charts()
