import matplotlib.pyplot as plt
from docx import Document
from docx.shared import Inches
from io import BytesIO


from visualisations.Preventivos import (
    generate_order_area_plot,
    generate_plagas_timeseries_facet,
    generate_total_plagas_trend_plot)

from visualisations.Roedores import (
    generate_roedores_station_status_plot,
    plot_tendencia_eliminacion_mensual)

from visualisations.Lamparas import (
    plot_estado_lamparas_por_mes,
    plot_estado_lamparas_con_leyenda,
    plot_capturas_especies_por_mes,
    plot_tendencia_total_capturas)



# Utilidad para agregar un gráfico de matplotlib directamente al doc
def add_plot_to_doc(doc, fig):
    """Add a matplotlib figure to a Word document"""
    if fig is None:
        print("Warning: Figure is None, skipping plot addition")
        return False

    try:
        with BytesIO() as image_stream:
            fig.savefig(image_stream, format='png', bbox_inches='tight', dpi=300)
            image_stream.seek(0)
            doc.add_picture(image_stream, width=Inches(5.5))
        plt.close(fig)
        return True
    except Exception as e:
        print(f"Error adding plot to document: {e}")
        if fig is not None:
            plt.close(fig)
        return False

# Función que genera el reporte completo y lo guarda en memoria
def generate_report_in_memory(df_preventivo, df_roedores, df_lamparas, sede: str):
    df_preventivo = df_preventivo[df_preventivo['Sede'] == sede].copy()
    df_roedores = df_roedores[df_roedores['Sede'] == sede].copy()
    df_lamparas = df_lamparas[df_lamparas['Sede'] == sede].copy()   

    doc = Document()
    doc.add_heading(f"Reporte Mensual {sede} - Serviplagas", level=1)

    # Sección Preventivos
    doc.add_heading("Preventivos 1", level=2)
    table_1, fig1 = generate_order_area_plot(df_preventivo)
    add_plot_to_doc(doc, fig1)

    # Add table
    t = doc.add_table(rows=1, cols=len(table_1.columns))
    t.style = 'Table Grid'
    hdr_cells = t.rows[0].cells
    for i, col in enumerate(table_1.columns):
        hdr_cells[i].text = str(col)
    for _, row in table_1.iterrows():
        row_cells = t.add_row().cells
        for i, val in enumerate(row):
            row_cells[i].text = str(val)


    doc.add_heading("Preventivos 2", level=2)
    table_2, fig2= generate_plagas_timeseries_facet(df_preventivo)
    add_plot_to_doc(doc, fig2)

    # Add table
    t = doc.add_table(rows=1, cols=len(table_2.columns))
    t.style = 'Table Grid'
    hdr_cells = t.rows[0].cells
    for i, col in enumerate(table_2.columns):
        hdr_cells[i].text = str(col)
    for _, row in table_2.iterrows():
        row_cells = t.add_row().cells
        for i, val in enumerate(row):
            row_cells[i].text = str(val)


    doc.add_heading("Preventivos 3", level=2)
    table_3, fig3 = generate_total_plagas_trend_plot(df_preventivo)
    add_plot_to_doc(doc, fig3)

    # Add table
    t = doc.add_table(rows=1, cols=len(table_3.columns))
    t.style = 'Table Grid'
    hdr_cells = t.rows[0].cells
    for i, col in enumerate(table_3.columns):
        hdr_cells[i].text = str(col)
    for _, row in table_3.iterrows():
        row_cells = t.add_row().cells
        for i, val in enumerate(row):
            row_cells[i].text = str(val)


    doc.add_heading("Roedores 1", level=2)
    table_1, fig1 = generate_roedores_station_status_plot(df_roedores)
    add_plot_to_doc(doc, fig1)

    # Add table
    t = doc.add_table(rows=1, cols=len(table_1.columns))
    t.style = 'Table Grid'
    hdr_cells = t.rows[0].cells
    for i, col in enumerate(table_1.columns):
        hdr_cells[i].text = str(col)
    for _, row in table_1.iterrows():
        row_cells = t.add_row().cells
        for i, val in enumerate(row):
            row_cells[i].text = str(val)



    doc.add_heading("Roedores 2", level=2)
    table_2, fig2= plot_tendencia_eliminacion_mensual(df_roedores)
    add_plot_to_doc(doc, fig2)

        # Add table
    t = doc.add_table(rows=1, cols=len(table_2.columns))
    t.style = 'Table Grid'
    hdr_cells = t.rows[0].cells
    for i, col in enumerate(table_2.columns):
        hdr_cells[i].text = str(col)
    for _, row in table_2.iterrows():
        row_cells = t.add_row().cells
        for i, val in enumerate(row):
            row_cells[i].text = str(val)

    doc.add_heading("Lámparas 1", level=2)
    table_1, fig2= plot_estado_lamparas_por_mes(df_lamparas)
    add_plot_to_doc(doc, fig2)

    # Add table
    t = doc.add_table(rows=1, cols=len(table_1.columns))
    t.style = 'Table Grid'
    hdr_cells = t.rows[0].cells
    for i, col in enumerate(table_1.columns):
        hdr_cells[i].text = str(col)
    for _, row in table_1.iterrows():
        row_cells = t.add_row().cells
        for i, val in enumerate(row):
            row_cells[i].text = str(val)


    doc.add_heading("Lámparas 2", level=2)
    table_2, fig2= plot_estado_lamparas_con_leyenda(df_lamparas)
    add_plot_to_doc(doc, fig2)

    # Add table
    t = doc.add_table(rows=1, cols=len(table_2.columns))
    t.style = 'Table Grid'
    hdr_cells = t.rows[0].cells
    for i, col in enumerate(table_2.columns):
        hdr_cells[i].text = str(col)
    for _, row in table_2.iterrows():
        row_cells = t.add_row().cells
        for i, val in enumerate(row):
            row_cells[i].text = str(val)



    doc.add_heading("Lámparas 3", level=2)
    table_3, fig2= plot_capturas_especies_por_mes(df_lamparas)
    add_plot_to_doc(doc, fig2)


        # Add table
    t = doc.add_table(rows=1, cols=len(table_3.columns))
    t.style = 'Table Grid'
    hdr_cells = t.rows[0].cells
    for i, col in enumerate(table_3.columns):
        hdr_cells[i].text = str(col)
    for _, row in table_3.iterrows():
        row_cells = t.add_row().cells
        for i, val in enumerate(row):
            row_cells[i].text = str(val)

    doc.add_heading("Lámparas 4", level=2)
    table_4, fig2= plot_tendencia_total_capturas(df_lamparas)
    add_plot_to_doc(doc, fig2)

        # Add table
    t = doc.add_table(rows=1, cols=len(table_4.columns))
    t.style = 'Table Grid'
    hdr_cells = t.rows[0].cells
    for i, col in enumerate(table_4.columns):
        hdr_cells[i].text = str(col)
    for _, row in table_4.iterrows():
        row_cells = t.add_row().cells
        for i, val in enumerate(row):
            row_cells[i].text = str(val)



    # Guardar el documento en disco
    output_path = f"outputs/reporte_serviplagas_{sede}.docx"
    doc.save(output_path)
    print(f" ✅  Reporte guardado en: {output_path}")