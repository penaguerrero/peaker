from pathlib import Path

from peaker.parse_xmls import parse_xmls
from peaker.plotting import mk_plots


def test_create_pdf(tmpdir):
    script_dir = Path(__file__).resolve().parent
    data_dir = script_dir / "Data"

    # Create the dictionary of the tests
    tests_ran, oldest_date, latest_date = parse_xmls(data_dir, "EST")

    # Make the plots
    plots = mk_plots(tests_ran, tmpdir)

    assert len(plots) == 5
