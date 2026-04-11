from pathlib import Path

from peaker.pdf_utils import create_pdf
from peaker.parse_xmls import parse_xmls
from peaker.table_utils import generate_report_table
from peaker.plotting import mk_plots


def test_create_pdf(tmpdir):
    script_dir = Path(__file__).resolve().parent
    data_dir = script_dir / "Data"

    # Set the function variables
    mission = "jwst"
    py_version = "py3.12"

    # Create the dictionary of the tests
    tests_ran, oldest_date, latest_date = parse_xmls(data_dir)

    # Create table of tests, versions, results, and print it in a csv file
    report_table = generate_report_table(mission, tmpdir, tests_ran, latest_date, oldest_date)

    # Make the plots
    plots = mk_plots(tests_ran, tmpdir)

    # Test the function
    create_pdf(mission, latest_date, oldest_date, py_version, tmpdir, report_table, plots)

    pdf_name = "report_peak_mem_" + py_version + ".pdf"
    pdf_path = tmpdir / pdf_name

    assert pdf_path.exists()
