import json
import logging
import os
import time
from datetime import timedelta, datetime, date

import yaml
from nsaph_utils.utils.io_utils import fopen, as_content


class AirNowDownloader:
    bbox = "-140.58788,20.634217,-60.119132,60.453505"

    format_csv = "text/csv"
    format_json = "application/json"
    datatype = "b"
    verbose = 1
    max_attempts = 5
    time_to_sleep_between_attempts = 10
    url = "https://www.airnowapi.org/aq/data/"

    @staticmethod
    def look_for_api_key():
        key = os.getenv('AIRNOWKEY', None)
        if key:
            logging.info("AirNow API Key has been found in the environment")
            return key
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
                key = content["api key"]
                logging.info("AIrNow API Key has been found in " + f)
                return key
        raise Exception("AirNow API Key was not found")

    def __init__(self, parameter: str, target: str, api_key: str = None):
        self.options = dict()
        self.options["bbox"] = self.bbox
        if ".json" in target.lower():
            self.options["format"] = self.format_json
        else:
            self.options["format"] = self.format_csv
        self.options["datatype"] = self.datatype
        self.options["verbose"] = self.verbose
        self.options["parameters"] = parameter
        self.target = target
        if api_key is None:
            api_key = self.look_for_api_key()
        self.options["api_key"] = api_key

    def reset(self):
        if os.path.exists(self.target):
            os.remove(self.target)

    def download(self, requested_date):
        is_json = self.options["format"] == self.format_json
        options = dict(self.options)
        options["startdate"] = str(requested_date) + "t00"
        options["enddate"] = str(requested_date + timedelta(days = 1)) + "t00"
        logging.debug("Requesting AirNowAPI data... Date = " + str(requested_date))
        with fopen(self.target, "at") as output:
            attempts = 0
            while True:
                try:
                    content = as_content(self.url, params=options, mode='t')
                    if is_json:
                        lines = json.loads(content)
                    else:
                        lines = content.split('\n')
                    for line in lines:
                        if is_json:
                            line = json.dumps(line)
                        output.write(line + '\n')
                    break
                except Exception as x:
                    attempts += 1
                    if attempts < self.max_attempts:
                        logging.warning(str(x))
                        time.sleep(self.time_to_sleep_between_attempts)
                        continue
                    raise

    def download_range(self, start_date, end_date = datetime.now().date()):
        dt = start_date
        t = datetime.now()
        year = dt.year
        month = dt.month
        logging.info("Starting download from: " + str(dt))
        while True:
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
    downloader = AirNowDownloader("no2", "airnow_no2.json.gz")
    downloader.reset()
    downloader.download_range(date(2020,1,1), date(2020,3,31))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    test()
