import csv
import json
import logging
import math
import os
import time
from datetime import timedelta, datetime, date

import pandas
import yaml
from nsaph_utils.utils.io_utils import fopen, as_content

from airnow_gis import GISAnnotator


class AirNowDownloader:
    SITE = "FullAQSCode"
    VALUE = "Value"
    GIS_COLUMNS = ["ZIP", "STATE", "GEOID"]
    bbox = "-140.58788,20.634217,-60.119132,60.453505"

    format_csv = "text/csv"
    format_json = "application/json"
    datatype = "b"
    verbose = 1
    max_attempts = 5
    time_to_sleep_between_attempts = 10
    url = "https://www.airnowapi.org/aq/data/"

    @staticmethod
    def get_config(key: str):
        candidates = [
            ".airnow.yaml",
            ".airnow.json",
            os.path.expanduser(".airnow.yaml"),
            os.path.expanduser(".airnow.json")
        ]
        for f in candidates:
            if os.path.exists(f):
                with open(f) as fp:
                    if f.endswith("yaml"):
                        content = yaml.safe_load(fp)
                    elif f.endswith(".json"):
                        content = json.load(fp)
                    else:
                        raise Exception(f)
                value = content[key]
                logging.info("AirNow {} has been found in {}".format(key, f))
                return value
        return None

    @staticmethod
    def look_for_api_key():
        key = os.getenv('AIRNOWKEY', None)
        if key:
            logging.info("AirNow API Key has been found in the environment")
            return key
        key = AirNowDownloader.get_config("api key")
        if key:
            return key
        raise Exception("AirNow API Key was not found")

    def __init__(self, target: str, parameter: str,
                 api_key: str = None):
        self.options = dict()
        self.options["bbox"] = self.bbox
        self.options["format"] = self.format_json
        self.options["datatype"] = self.datatype
        self.options["verbose"] = self.verbose
        self.options["parameters"] = parameter
        self.target = target
        if api_key is None:
            api_key = self.look_for_api_key()
        self.options["api_key"] = api_key
        shapes = self.get_config("shapes")
        if not shapes:
            raise Exception("Shape files are not specified")
        self.annotator = GISAnnotator(shapes, self.GIS_COLUMNS)
        self.sites = dict()
        self.columns = None

    def reset(self):
        if os.path.exists(self.target):
            os.remove(self.target)
        self.columns = None

    def download(self, requested_date):
        is_json = ".json" in self.target
        options = dict(self.options)
        options["startdate"] = str(requested_date) + "t00"
        #options["enddate"] = str(requested_date + timedelta(days = 1)) + "t00"
        options["enddate"] = str(requested_date) + "t23:59"
        logging.debug("Requesting AirNowAPI data... Date = " + str(requested_date))
        with fopen(self.target, "at") as output:
            attempts = 0
            while True:
                try:
                    content = as_content(self.url, params=options, mode='t')
                    break
                except Exception as x:
                    attempts += 1
                    if attempts < self.max_attempts:
                        logging.warning(str(x))
                        time.sleep(self.time_to_sleep_between_attempts)
                        continue
                    raise
            rows = self.process(content)
            if not rows:
                raise Exception("Empty response for " + str(requested_date))
            if is_json:
                for row in rows:
                    json.dump(row, output)
                    output.write('\n')
            else:
                self.dump_csv(output, rows)

    @staticmethod
    def dump_csv(output, rows):
        row = rows[0]
        writer = csv.DictWriter(output, row.keys(), delimiter=',',
                                quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        writer.writerows(rows)

    def process(self, content: str):
        df = pandas.read_json(content)
        agg = {
            c: "mean" if c == self.VALUE else "first"
            for c in df.columns if c != self.SITE
        }
        aggregated = df.groupby(self.SITE).agg(agg).reset_index()
        self.check_sites(aggregated)
        data = []
        for _, row in aggregated.iterrows():
            record = {column: row[column] for column in aggregated.columns}
            site = record[self.SITE]
            record.update(self.sites[site])
            data.append(record)
        return data

    def check_sites(self, df: pandas.DataFrame):
        sites = df[self.SITE]
        new_monitors = {m for m in sites if m not in self.sites}
        if not new_monitors:
            return
        x = "Longitude"
        y = "Latitude"
        sites = df[[self.SITE, x, y]]
        sites = sites[sites[self.SITE].isin(new_monitors)]
        annotated = self.annotator.join(sites, x = x, y = y)
        for _, site in annotated.iterrows():
            row = {
                key: site[key] if not (
                        isinstance(site[key], float) and math.isnan(site[key])
                ) else None
                for key in self.GIS_COLUMNS
            }
            row[self.SITE] = site[self.SITE]
            fips5 = row["GEOID"]
            del row["GEOID"]
            row["FIPS5"] = fips5
            self.sites[site[self.SITE]] = row
        return

    def download_range(self, start_date, end_date = datetime.now().date()):
        dt = start_date
        year = dt.year
        month = dt.month
        logging.info("Starting download from: " + str(dt))
        while True:
            t = datetime.now()
            self.download(dt)
            if dt >= end_date:
                break
            dt += timedelta(days = 1)
            if dt.month != month:
                logging.info("{:d}-{:d}".format(year, month))
            month = dt.month
            year = dt.year
            elapsed = datetime.now() - t
            if elapsed.total_seconds() < 7.2:
                time.sleep(7.2 - elapsed.total_seconds())
        logging.info("Download complete. Last downloaded date: {}".format(str(dt)))


def test():
    downloader = AirNowDownloader("airnow_no2.json.gz", "no2")
    downloader.reset()
    downloader.download_range(date(2019,9,1), date(2019,12,31))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test()
