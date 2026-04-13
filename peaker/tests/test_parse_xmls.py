from pathlib import Path
from datetime import datetime, timezone

from peaker.parse_xmls import parse_xmls


def test_parse_xmls():
    script_dir = Path(__file__).resolve().parent
    data_dir = script_dir / "Data"

    # Test the function
    tests_ran, oldest_date, latest_date = parse_xmls(data_dir)

    # Set the expected oldest and latest dates
    date_format = "%Y-%m-%d"
    expected_oldest_date = datetime.strptime("2026-02-09", date_format).astimezone(timezone.utc)
    expected_latest_date = datetime.strptime("2026-02-13", date_format).astimezone(timezone.utc)
    # Make sure the dates are in local time
    expected_oldest_date = expected_oldest_date.astimezone().date()
    expected_latest_date = expected_latest_date.astimezone().date()

    assert len(tests_ran) == 5
    assert oldest_date == expected_oldest_date
    assert latest_date == expected_latest_date
