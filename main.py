import logging

import click

from pathlib import Path
from urllib.parse import urlparse

from src.Download import DownloadManager
from src import GoogleImage


@click.command()
@click.option('--search', '-s', help='Search term', type=str, required=True)
@click.option('--number', '-n', default=10, help='Number of images to download', type=int)
def main(search: str, number: int):
    if not Path('./images').exists():
        Path('./images').mkdir()
    download_manager: DownloadManager = DownloadManager()
    images = GoogleImage.search(search, number)
    [download_manager.add(image, Path('./images') / urlparse(image).path.split('/')[-1]) for image in images]
    download_manager.start()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
