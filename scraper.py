from dataclasses import dataclass
import re
import sys
import requests
from lxml import html
import os
import praw

from helper_functions import get_image_from_url, save_image


    

class Scraper:
    # _image_exts = ['.jpg', '.jpeg', '.gif', '.png']
    _regex_image_exts = re.compile(r'.(jpg|jpeg|gif|png)$')
    _regex_image_galleries = re.compile(r'gallery\/(.*)')

    def __init__(self, api_config: dict, subreddit: str) -> None:
        self.subreddit = subreddit
        self._images_urls = None
        self._api = praw.Reddit(**api_config)
        self._subreddit = self._api.subreddit(subreddit)

    def is_gallery_or_image(self, url: str) -> bool:
        """ Takes a url as a string and returns a True for those that are images and galleries, False for those
        that are not """
        if self._regex_image_exts.search(url) or self._regex_image_galleries.search(url):
            return True
        return False

    def get_top_submissions(self, time_span: str):
        return self._subreddit.top(time_span)

    def get_top_image_submissions(self, time_span: str) -> dict:
        submissions = self.get_top_submissions(time_span)
        return [i for i in submissions if self.is_gallery_or_image(i.url)]

    def _compile_image_links(self, submissions) -> list:
        results = []
        for submission in submissions:
            if self._regex_image_exts.search(submission.url):
                results.append(submission.url)
            elif self._regex_image_galleries.search(submission.url):
                gallery_images = self._get_imgur_gallery_links(submission.url)
                results.append(gallery_images)


    def _get_imgur_gallery_links(self, gallery_address: str):
        """ Takes an imgur gallery address and returns a list of all image urls in the gallery"""
        print(gallery_address)
        gallery = requests.get(gallery_address)

        if gallery.status_code == 200:
            gallery_page = html.fromstring(gallery.text)
            gallery_image_urls = gallery_page.xpath('//div[@class="image textbox "]/a/@href')
            # replaces the 'http:' which is absent from imgur links
            gallery_image_urls = ['http:' + i for i in gallery_image_urls]
            return gallery_image_urls
        else:
            print('Bad response from gallery server.')
            sys.exit()


    def save_pics_to(self, submissions: list, save_dir: str="./images"):
        compiled_subs = self._compile_image_links(submissions)
        for submission in compiled_subs:
            image = get_image_from_url(submission.url)
            extension = self._regex_image_exts.match(submission.url)
            save_directory = os.path.join(save_dir, extension)
            save_image(save_dir, image, submission.name, save_directory)
