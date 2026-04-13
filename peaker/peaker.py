"""Main module"""

import sys
import argparse
from datetime import datetime, timedelta, UTC, timezone
from pathlib import Path

from peaker.get_artifacts import get_artifacts
from peaker.parse_xmls import parse_xmls
from peaker.plotting import mk_plots
from peaker.table_utils import generate_report_table
from peaker.pdf_utils import create_pdf
from peaker.jwst_utils import ART_JWST_REPO, POOLS_JWST
from peaker.roman_utils import ART_ROMAN_REPO, POOLS_ROMAN
from peaker.utils import TIMEZONES


def main():
    parser = argparse.ArgumentParser(description="Display peak memory history for Regression Tests.")
    parser.add_argument("art_credentials",
                        action="store",
                        help="File with Artifactor credentials.")
    parser.add_argument("--xmldir", "-x",
                        action="store",
                        default=None,
                        help="Path of the directory to save/read the XML files.")
    parser.add_argument("--mission", "-m",
                        action="store",
                        default="jwst",
                        help="Name of the mission to analyze, i.e. -m=jwst")
    parser.add_argument("--days", "-d",
                        action="store",
                        default=None,
                        type=int,
                        help="Number of days to show, e.g. -d=5 will show today and the last 4 days back.")
    parser.add_argument("--period", "-p",
                        action="store",
                        default=None,
                        help="Period of time to show, input should be in the format year-month-day, "
                             "local time, e.g. -p=2026-01-23to2026-02-27")
    parser.add_argument("--timezone", "-t",
                        dest="localtimezone",
                        action="store",
                        default="EST",
                        help="Timezone to convert UTC time from xml files in the plots and report, "
                             "e.g. -t=GMT")
    parser.add_argument("--version", "-v",
                        dest="py_version",
                        action="store",
                        default="3.12",
                        help="Python version of the results to get via xml files, e.g. -v=3.11")
    parser.add_argument("-s",
                        dest="skip_download_artifacts",
                        action="store_true",
                        default=False,
                        help="Use flag -s to skip downloading artifacts and just read from xmldir.")

    args = parser.parse_args()

    # Define variables
    credentials_file = args.art_credentials
    xmldir = args.xmldir
    mission = args.mission
    days = args.days
    period = args.period
    localtimezone = args.localtimezone
    py_version = "py" + args.py_version
    skip_download_artifacts = args.skip_download_artifacts

    # Set the local timezone
    if localtimezone in TIMEZONES:
        localtz = TIMEZONES[localtimezone]
    else:
        localtz = "America/New_York"
    print("Local timezone set to {}".format(localtz))

    # Get the path where to find xml files
    if xmldir is not None:
        xmldir = Path(xmldir)

    # Get the appropriate Artifactory repo name and the
    # corresponding description of pool tests
    if mission == "jwst":
        art_repo = ART_JWST_REPO
        pools = POOLS_JWST
    elif mission == "roman":
        art_repo = ART_ROMAN_REPO
        pools = POOLS_ROMAN

    # Set the start and end dates in UTC
    start_date, end_date = None, None
    if days is not None:
        start_date = datetime.now(UTC) - timedelta(days=days)
        end_date = datetime.now(UTC)
    elif period is not None:
        start_date = period.split("to")[0]
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        start_date = start_date.astimezone(timezone.utc)
        end_date = period.split("to")[1]
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        end_date = end_date.astimezone(timezone.utc)

    # Get relevant xml files from artifactory
    if not skip_download_artifacts:
        outdir = get_artifacts(credentials_file, art_repo, py_version,
                               outdir=xmldir, start_date=start_date, end_date=end_date)
    else:
        if xmldir is None:
            raise ValueError("No XML directory specified.")
        outdir = xmldir

    # Store memory info in a dictionary of test name and points per date
    tests_ran, local_sdate, local_edate = parse_xmls(outdir, localtz)

    # Create table of tests, versions, results, and print it in a csv file
    report_table = generate_report_table(mission, outdir, tests_ran, local_sdate, local_edate, pools=pools)

    # Make the plots
    plots = mk_plots(tests_ran, outdir)

    # Create PDF report with table and plots
    create_pdf(mission, local_sdate, local_edate, py_version, outdir, report_table, plots)

    print("\nFinished! \n")


if __name__ == "__main__":
    sys.exit(main())
