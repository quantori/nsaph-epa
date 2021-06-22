"""
Python module to download EPA AirNow Data using WebServices API

https://docs.airnowapi.org/webservices

AirNow contains real-time up-to-date pollution data but is less reliable
than AQS

"""
import logging
from datetime import datetime

from airnow_downloader import AirNowDownloader
from airnow_ds_def import AirNowContext


class AirNow:
    """
    Main class
    """

    def __init__(self, context: AirNowContext = None):
        if not context:
            context = AirNowContext(__doc__)
        self.context = context

        self.start = datetime.strptime(context.start_date, "%Y-%m-%d").date()
        self.end = datetime.strptime(context.end_date, "%Y-%m-%d").date()
        self.downloader = AirNowDownloader(
            parameter=self.context.parameters,
            target=context.destination,
            qc=context.qc
        )

    def download(self):
        if self.context.reset:
            self.downloader.reset()
        self.downloader.download_range(self.start, self.end)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    downloader = AirNow()
    downloader.download()
