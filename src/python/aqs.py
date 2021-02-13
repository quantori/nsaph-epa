"""
Python module to download EPA AQS Data hosted at https://www.epa.gov/aqs

The utility expects user to specify a list of years, a list of
EPA Parameter Codes (see https://www.epa.gov/aqs/aqs-code-list)
and some instructions how to format output

The data is downloaded from \
https://aqs.epa.gov/aqsweb/airdata/download_files.html

The tool also adds a column containing a uniquely generated Monitor Key

"""

from aqs_ds_def import AQSContext
from aqs_tools import collect_aqs_download_tasks, download_data


class AQS:
    """
    Main class, describes the whole download job
    """
    def __init__(self, context: AQSContext = None):
        """
        Creates a new instance
        :param context: An optional AQSContext object, if not specified,
            then it is constructed from the command line arguments
        """
        if not context:
            context = AQSContext(__doc__)
        self.context = context
        self.download_tasks = None

    def collect_downloads(self):
        """
        Constructs a list of all download tasks necessary to execute to
        download all the data defined in the configuration ()
        :return: Nothing
        """
        self.download_tasks = collect_aqs_download_tasks(self.context)

    def is_downloaded(self):
        """
        Checks if there anything remains to be downloaded or if all
        files are up to date
        :return: True if everything is up to date, False otherwise
        """
        if not self.download_tasks:
            self.collect_downloads()
        for task in self.download_tasks:
            if not task.is_up_to_date():
                return False
        return True

    def clear(self):
        """
        Removes all previously downloaded data from the local storage
        :return: Nothing
        """
        if not self.download_tasks:
            self.collect_downloads()
        for task in self.download_tasks:
            task.reset()

    def download(self):
        """
        Downloads all remaining data absent or not up to date)
        :return: Nothing
        """
        if not self.download_tasks:
            self.collect_downloads()
        for task in self.download_tasks:
            if task.is_up_to_date():
                continue
            download_data (task)


if __name__ == '__main__':
    downloader = AQS()
    print(downloader.context)
    print("Up to date: " + str(downloader.is_downloaded()))
    downloader.download()
    print("Up to date: " + str(downloader.is_downloaded()))


