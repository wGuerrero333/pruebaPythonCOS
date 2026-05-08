#!/usr/bin/env python3
import logging
import sys
from datetime import datetime
from fpdf import FPDF
from fpdf.table import FontFace
from fpdf.enums import TextEmphasis
from modules.db_handler import leer_desde_mysql

OUTPUT_PDF = "data/reporte_final.pdf"


class PDFReporte(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Courier", "I", 8)
        self.set_text_color(0, 51, 153)
        self.cell(0, 10, f"Pag. {self.page_no()}/{{nb}}", align="C")


def generar_pdf():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    registros = leer_desde_mysql()
    if not registros:
        print("No hay datos en MySQL para generar el PDF.")
        return False

    pdf = PDFReporte(orientation="L", format="A4")
    pdf.set_margins(18, 15, 18)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.set_font("Courier", "B", 16)
    pdf.set_text_color(0, 51, 153)
    pdf.cell(0, 12, "Reporte de Ordenes Procesadas - RPA", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Courier", "", 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 7, f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(2)
    pdf.set_draw_color(0, 51, 153)
    pdf.set_line_width(0.5)
    y = pdf.get_y()
    pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
    pdf.ln(8)

    headers = ["#", "Orden ID", "Estado API", "Titulo del Libro", "Precio", "Disponibilidad", "Fecha Proc."]
    col_widths = [12, 22, 34, 82, 28, 32, 38]
    available_width = pdf.w - pdf.l_margin - pdf.r_margin

    total_w = sum(col_widths)
    col_widths = [w * available_width / total_w for w in col_widths]

    headings_style = FontFace(
        family="Courier",
        emphasis=TextEmphasis.B,
        color=(255, 255, 255),
        fill_color=(0, 51, 153)
    )

    pdf.set_font("Courier", "", 9)
    pdf.set_text_color(0, 0, 0)

    with pdf.table(
        first_row_as_headings=True,
        borders_layout="ALL",
        align="LEFT",
        text_align="LEFT",
        col_widths=col_widths,
        repeat_headings=1,
        headings_style=headings_style,
    ) as table:
        header = table.row()
        for h in headers:
            header.cell(h)

        for r in registros:
            row = table.row()
            row.cell(str(r.get("id", "")))
            row.cell(str(r.get("orden_id", "")))

            estado = r.get("estado_api", "")
            if estado == "Aprobada":
                pdf.set_text_color(0, 102, 204)
            elif estado == "Error_A":
                pdf.set_text_color(0, 51, 102)
            elif estado == "En revisi\xf3n":
                pdf.set_text_color(51, 102, 153)
            row.cell(estado)
            pdf.set_text_color(0, 0, 0)

            row.cell(str(r.get("titulo_libro", "")))
            row.cell(str(r.get("precio", "")))
            row.cell(str(r.get("disponibilidad", "")))
            fecha = r.get("fecha_procesamiento", "")
            row.cell(str(fecha) if fecha else "")

    pdf.ln(5)
    pdf.set_font("Courier", "B", 10)
    pdf.set_text_color(0, 51, 153)
    pdf.cell(0, 8, f"Total de registros: {len(registros)}", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.output(OUTPUT_PDF)
    print(f"PDF generado exitosamente: {OUTPUT_PDF}")
    return True


if __name__ == "__main__":
    exito = generar_pdf()
    sys.exit(0 if exito else 1)
