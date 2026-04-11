from pathlib import Path
from datetime import datetime

from peaker.parse_xmls import parse_xmls


def test_parse_xmls():
    script_dir = Path(__file__).resolve().parent
    data_dir = script_dir / "Data"

    # Test the function
    tests_ran, oldest_date, latest_date = parse_xmls(data_dir)

    date_format = "%Y-%m-%d"
    expected_oldest_date = datetime.strptime("2026-02-09", date_format).date()
    expected_latest_date = datetime.strptime("2026-02-13", date_format).date()

    assert len(tests_ran) == 5
    assert oldest_date == expected_oldest_date
    assert latest_date == expected_latest_date
