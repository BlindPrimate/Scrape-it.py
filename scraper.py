from dataclasses import dataclass
import sys
import requests
from lxml import html
import praw

from helper_functions import save_image

    

class Scraper:
    _image_exts = ['.jpg', '.jpeg', '.gif', '.png']

    def __init__(self, config: dict, subreddit: str) -> None:
        self.subreddit = subreddit
        self.images_urls = None
        self.api = praw.Reddit(**config)

    def is_image(self, url):
        """ Takes a url as a string and returns a True for those that are images, False for those
        that are not """
        if any(image_ext in url for image_ext in self._image_exts):
            return True
        return False

    def get_image_urls(self, url):
        # pulls html text from url 
        response = requests.get(url)

        # checks for good response from server
        if response.status_code == 200:
            # converst html into xml 
            print(response.text)
            page = html.fromstring(response.text)
            
            # creates list of all post title links
            urls = page.xpath('//p[@class="title"]/a/@href')

            # checks to see which of the urls are galleries and scrapes the image
            # links of those that are
            image_urls = []
            for url in urls:
                if self.is_image(url):
                    image_urls.append(url)                      
                else:
                    image_urls.extend(self.get_imgur_gallery_links(url))
            return image_urls 
        else:
            print('Bad response from reddit server.')
            sys.exit()

            
    def get_imgur_gallery_links(self, gallery_address):
        """ Takes an imgur gallery address and returns a list of all image urls in the gallery"""
        image_urls = []
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


    def save_top_pics(self, subreddit, save_dir):
        urls = self.get_image_urls('http://www.reddit.com/r/' + subreddit + '/top')
        print('Saving ' + str(len(urls)) + ' images...')
        # iterates through image_urls and saves each image
        count = 0
        for i in urls:
            while not self.is_image(i):
                i = i[:-1]
            count += 1
            image_file = requests.get(i)
            filename = 'image-' + str(count)
            if i.endswith('.jpg'):
                save_image(save_dir, image_file.content, filename, '.jpg')
            elif i.endswith('.jpeg'):
                save_image(save_dir, image_file.content, filename, '.jpeg')
            elif i.endswith('.gif'):
                save_image(save_dir, image_file.content, filename, '.gif')
            elif i.endswith('.png'):
                save_image(save_dir, image_file.content, filename, '.png')
