import threading
import requests
import logging

from time import sleep
from typing import List, Tuple
from pathlib import Path


class DownloadThread(threading.Thread):
    def __init__(self, url: str, path: Path):
        """
        :param url: the url to download from
        :param path: the path to save the file to
        """
        threading.Thread.__init__(self)
        self.url: str = url
        self.path: Path = path

    def run(self):
        """
        Download the file from `url` and save it locally under `file_name`:
        """
        r = requests.get(self.url, stream=True)  # create HTTP response object
        if r.status_code != 200:
            logging.error(f'Error downloading {self.url}! Status code: {r.status_code}')
            return  # Error
        if self.path.exists():
            logging.warning(f'File {self.path} already exists!')
            return  # File already exists
        logging.info(f'Downloading {self.url} to {self.path}...')
        with open(self.path, 'wb') as f:  # open in binary mode
            for chunk in r.iter_content(chunk_size=1024):  # 1024 bytes
                if chunk:
                    f.write(chunk)
                    f.flush()
        logging.info(f'Finished downloading {self.url} to {self.path}!')


class DownloadManager:
    class Daemon(threading.Thread):
        def __init__(self, parent: 'DownloadManager'):
            threading.Thread.__init__(self)
            self.parent: DownloadManager = parent

        def run(self):
            while True:
                if len(self.parent.threads) < self.parent.max_threads:  # Check if we can start a new thread
                    # Check if there are any tasks to do
                    if len(self.parent.tasks) > 0:
                        task = self.parent.tasks.pop(0)
                        thread = DownloadThread(task[0], task[1])
                        thread.start()
                        self.parent.threads.append(thread)
                    else:
                        # No tasks to do, so stop the daemon
                        return
                else:
                    # Check if any threads have finished
                    self.parent.threads = [thread for thread in self.parent.threads if thread.is_alive()]
                sleep(0.1)

    def __init__(self, max_threads: int = 5):
        """
        :param max_threads: the maximum number of threads to use
        """
        self.max_threads: int = max_threads
        self.threads: List[DownloadThread] = []
        self.tasks: List[Tuple[str, Path]] = []
        self.daemon: DownloadManager.Daemon = DownloadManager.Daemon(self)

    def add(self, url: str, path: Path):
        self.tasks.append((url, path))

    def start(self):
        self.daemon.start()
