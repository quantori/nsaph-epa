from aqs_ds_def import AQSContext
from aqs_tools import collect_aqs_download_tasks, download_data


class AQS:
    def __init__(self, context: AQSContext):
        self.context = context
        self.download_tasks = None

    def collect_downloads(self):
        self.download_tasks = collect_aqs_download_tasks(self.context)

    def is_downloaded(self):
        if not self.download_tasks:
            self.collect_downloads()
        for task in self.download_tasks:
            if not task.is_up_to_date():
                return False
        return True

    def download(self):
        if not self.download_tasks:
            self.collect_downloads()
        for task in self.download_tasks:
            if task.is_up_to_date():
                continue
            download_data (task)


if __name__ == '__main__':
    context = AQSContext()
    print(context)
    downloader = AQS(context)
    print("Up to date: " + str(downloader.is_downloaded()))
    downloader.download()
    print("Up to date: " + str(downloader.is_downloaded()))


