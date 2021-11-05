"""
Python module to download EPA AirNow Data using WebServices API

https://docs.airnowapi.org/webservices

AirNow contains real-time up-to-date pollution data but is less reliable
than AQS

"""
import os

import logging
from datetime import datetime
import fiona

from epa.airnow_downloader import AirNowDownloader
from epa.airnow_ds_def import AirNowContext
from nsaph import init_logging


class AirNow:
    """
    Main class
    """

    def __init__(self, context: AirNowContext = None):
        init_logging()
        if not context:
            context = AirNowContext(__doc__)
        self.context = context
        if self.context.destination is None:
            self.context.destination = os.curdir
        if self.context.cfg and self.context.cfg != ".airnow.yaml":
            os.system("cp {} .airnow.yaml".format(self.context.cfg))
        if self.context.shape_dir:
            if not os.path.isdir(self.context.shape_dir):
                raise ValueError(self.context.shape_dir)
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
