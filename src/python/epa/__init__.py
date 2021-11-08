import datetime
from typing import Dict

RECORD_NUM_FORMAT = "{:d}-{:010d}"
STATE_CODE = "State Code"
COUNTY_CODE = "County Code"
SITE_NUM = "Site Num"
PARAMETER_CODE = "Parameter Code"
MONITOR = "Monitor"
RECORD = "Record"


def add_record_num(row: Dict, record_index: int):
    year = None
    if "Year" in row:
        year = int(row["Year"])
    else:
        for column in ["Date Local", "UTC"]:
            if column in row:
                dt = datetime.datetime.fromisoformat(row[column])
                year = dt.year
                break
    if not year:
        raise ValueError("No information about year")
    r = RECORD_NUM_FORMAT.format(year, record_index)
    row[RECORD] = r
