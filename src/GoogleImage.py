import os
import requests
import logging

from typing import List

API_KEY = os.getenv('SERPAPI_KEY')
API_URL = 'https://serpapi.com/search.json?q={}&engine=google_images&ijn={}&api_key={}'


def search(query: str, num: int = 10) -> List[str]:
    """
    Get image urls from Google Image Search
    :param query: query string
    :param num: number of images to get
    :return: list of image urls
    """
    logging.info(f'Searching for {num} images...')
    urls = []
    search_num = num // 100  # 100 images per page
    for i in range(search_num + 1):
        response = requests.get(API_URL.format(query, i, API_KEY))  # create HTTP response object
        data = response.json()
        try:
            if data['error']:
                logging.error(data['error'])
                return []
        except KeyError:
            pass
        [urls.append(result['original']) for result in data['images_results']]
    logging.info(f'Found {len(urls)} images')
    return urls[:num]
