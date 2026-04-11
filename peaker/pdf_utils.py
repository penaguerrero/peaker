"""Utilities to create a PDF report with plots and a table."""

import os
from fpdf import FPDF


def _get_plt_path(plots, test_name, test_class):
    plt_name = None
    for plt in plots:
        plt_basename = os.path.basename(plt)
        if test_name in plt_basename and test_class in plt_basename:
            plt_name = plt
            break
    return plt_name


def _select_cols(report_table):
    # Select the columns and add the column name to later append the page numbers of the plot location
    selected_cols = []
    headers = ["Test Name", "Instrument Mode", "Units", "Latest Peak Mem",
               "Data Points", "End Median - Start Median", "Plot Page"]
    for i in range(len(report_table["Test_name"])):
        if i == 0:
            selected_cols.append(headers)
        row = [
            str(report_table["Test_name"][i]),
            str(report_table["Instrument_mode"][i]),
            str(report_table["Units"][i]),
            str(report_table["Latest_peakmem"][i]),
            str(report_table["Data_points"][i]),
            str(report_table["Diff_medians"][i]),
            ]
        selected_cols.append(row)

    # The table format for the PDF can adjust the column width size with a tuple
    # called col_widths. Each number is a percentage of the total page
    # width, and the tuple should add up to 100.
    col_widths = (37, 23, 7, 9, 8, 9, 7)

    # Sanity checks
    if len(headers) != len(col_widths):
        raise ValueError("Inconsistent number of columns and widths in PDF table.")
    if sum(col_widths) != 100:
        raise ValueError("Inconsistent column widths in PDF table.")
    
    return selected_cols, col_widths


def create_pdf(mission, start_date, end_date, py_version, outdir, report_table, plots):
    """
    Creates a PDF report with plots and a table.
    
    Parameters
    ----------
    mission : str
        Mission name.
    start_date : datetime.date
        Start date of testing period in local timezone.
    end_date : datetime.date
        End date of testing period in local timezone.
    py_version : str
        Version of Python tested and reported. 
    outdir : pathlib.Path
        Full path for the output directory.
    report_table : astropy Table
        Contains all data to report in the table
    plots : list
        Strings of full paths and names of the plots to include in the report. 

    Returns
    -------
    Nothing
    
    """
    
    # Get selected data from table
    selected_cols, col_widths = _select_cols(report_table)
    try:
        classnames = report_table["Class"]
    except KeyError:
        classnames = report_table["Instrument_mode"]

    # Create an instance of an FPDF class.
    pdf = FPDF()

    # Define font type and size
    pdf_font = "Arial"
    main_title_font_size = 16
    sub_title_font_size = 13
    body_font_size = 9

    # Add content to the PDF
    
    pdf.add_page()  # Add a new page.
    pdf.set_font(pdf_font, size=main_title_font_size)  # Set the font for text.
    title = "{} Regression Tests Memory Peaks from \n {} to {}".format(
        mission.upper(), start_date, end_date)
    pdf.multi_cell(w=0, h=10, text=title, ln=True, align="C")

    # First page: worse performance, highest memory peak increment
    pdf.set_font(pdf_font, size=body_font_size)
    page_counter = 1
    pdf.set_y(45)

    # These are all the cell parameters that can be modified:
    # Cell(width, height, text, border (0=no, 1=yes),
    #      line break (0=right, 1=next line), align ('L', 'C', 'R'))
    text = "Test with the highest memory peak **increment**:  {}".format(report_table["Test_name"][0])
    pdf.cell(w=0, h=10, text=text, ln=True, align="L")
    text = "  - Instrument mode:  {}".format(report_table["Instrument_mode"][0])
    pdf.cell(w=0, h=10, text=text, ln=True, align="L")
    text = " - Memory Peak increased from beginning of period by:  {} {}".format(
        report_table["Diff_medians"][0], report_table["Units"][0])
    pdf.cell(w=0, h=10, text=text, ln=True, align="L")
    plt_name = _get_plt_path(plots, report_table["Test_name"][0], classnames[0])
    pdf.image(plt_name, x=5, y=80, w=200)  # Add an image to the page.
    pdf.set_y(265)
    pdf.cell(200, 10, txt=f"Page {page_counter}", ln=True, align='C')
    # Update the first table entry
    selected_cols[1].append(str(page_counter))
    # Increase the page counter
    page_counter += 1

    # Second page: best performance, highest memory peak decrement
    pdf.add_page()
    pdf.set_y(30)
    text = "Test with the highest memory peak **improvement**: {}".format(report_table["Test_name"][-1])
    pdf.cell(w=0, h=10, text=text, ln=True, align="L")
    text = "  - Instrument mode:  {}".format(report_table["Instrument_mode"][-1])
    pdf.cell(w=0, h=10, text=text, ln=True, align="L")
    text = " - Memory Peak increased from beginning of period by:  {} {}".format(
        report_table["Diff_medians"][-1], report_table["Units"][-1])
    pdf.cell(w=0, h=10, text=text, ln=True, align="L")
    plt_name = _get_plt_path(plots, report_table["Test_name"][-1], classnames[-1])
    pdf.image(plt_name, x=5, y=70, w=200)
    pdf.set_y(265)
    pdf.cell(200, 10, txt=f"Page {page_counter}", ln=True, align='C')
    # Update the last table entry
    selected_cols[-1].append(str(page_counter))
    # Increase the page counter
    page_counter += 1

    # Pages with all other plots for increments
    # in the loop exclude the first and last entries
    for i in range(1, len(report_table["Test_name"])-1, 2):
        pdf.add_page()
        table_row = i + 1

        # Only at top of the third page, add subtitle
        if i == 1:
            pdf.set_y(265)
            pdf.cell(200, 10, txt=f"Page {page_counter}", ln=True, align='C')
            pdf.set_y(18)
            pdf.set_font(pdf_font, size=sub_title_font_size)
            text = "The following pages present other changes in memory peak"
            pdf.cell(w=0, h=10, text=text, ln=True, align="L")
        pdf.set_font(pdf_font, size=body_font_size)

        # First plot in this page
        pdf.set_y(30)
        text = "Test name: {}".format(report_table["Test_name"][i])
        pdf.cell(w=0, h=10, text=text, ln=True, align="L")
        text = "  - Instrument mode: {}".format(report_table["Instrument_mode"][i])
        pdf.cell(w=0, h=10, text=text, ln=True, align="L")
        text = " - Peak memory change: {} {}".format(
            report_table["Diff_medians"][i], report_table["Units"][i])
        pdf.cell(w=0, h=10, text=text, ln=True, align="L")
        plt_name = _get_plt_path(plots, report_table["Test_name"][i], classnames[i])
        pdf.image(plt_name, x=65, y=50, w=115)
        # Add the page number where the plot can be found
        selected_cols[table_row].append(str(page_counter))

        # Second test plot in the same page
        if len(report_table["Test_name"])-1 > i + 1:
            pdf.set_y(145)
            text = "Test name: {}".format(report_table["Test_name"][i+1])
            pdf.cell(w=0, h=10, text=text, ln=True, align="L")
            text = "  - Instrument mode: {}".format(report_table["Instrument_mode"][i+1])
            pdf.cell(w=0, h=10, text=text, ln=True, align="L")
            text = " - Peak memory change: {} {}".format(
                report_table["Diff_medians"][i+1], report_table["Units"][i+1])
            pdf.cell(w=0, h=10, text=text, ln=True, align="L")
            plt_name = _get_plt_path(plots, report_table["Test_name"][i+1], classnames[i+1])
            pdf.image(plt_name, x=65, y=165, w=115)
            # Add the page number where the plot can be found
            selected_cols[table_row+1].append(str(page_counter))

        # Increase the page counter
        pdf.set_y(265)
        pdf.cell(200, 10, txt=f"Page {page_counter}", ln=True, align='C')
        page_counter += 1

    # Add table
    pdf.add_page()
    pdf.set_y(30)
    pdf.set_font(pdf_font, size=body_font_size)
    greyscale = 200
    with pdf.table(width=160, col_widths=col_widths,
                   cell_fill_color=greyscale, cell_fill_mode="ROWS") as table:
        for data_row in selected_cols:
            row = table.row()
            for datum in data_row:
                row.cell(datum)

    # Output the PDF to a file.
    pdf_name = "report_peak_mem_" + py_version + ".pdf"
    pdf_path = outdir / pdf_name
    pdf.output(pdf_path)
    
    print("\nPDF generated successfully: {}".format(pdf_path))
