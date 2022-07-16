import re
import os
import praw
from concurrent.futures import ThreadPoolExecutor

from helper_functions import get_image_from_url, make_dir_if_not_exist, save_image


class Scraper:
    """
    Provides API to pull images from a given subreddit.

    Args:
        api_config (dict): dictionary object containing basic auth data for reddit API
        subreddit (str): target subreddit
        logging (bool): enable logging
    
    """
    _regex_image_exts = re.compile(r'.(jpg|jpeg|gif|png)')

    def __init__(self, api_config: dict, subreddit: str, logging=False) -> None:
        self.subreddit = subreddit
        self._logging = logging
        self._api = praw.Reddit(**api_config)
        self._subreddit = self._api.subreddit(subreddit)

    def is_gallery_or_image(self, submission) -> bool:
        """Takes a url as a string and returns a True for those that are images and galleries, False for those
        that are not."""
        if hasattr(submission, 'post_hint') or hasattr(submission, 'is_gallery'):
            return True
        return False

    def get_top_submissions(self, time_span: str):
        """Pull top submission objects from the subreddit."""
        return self._subreddit.top(time_span)

    def get_top_image_submissions(self, time_span: str) -> dict:
        """Pull top submission objects that are images from the subreddit."""
        submissions = self.get_top_submissions(time_span)
        if self._logging:
            print("Retreiving images...")
        return [i for i in submissions if self.is_gallery_or_image(i)]


    def _get_gallery_urls(self, submission):
        """Retreive gallery images contained in a gallery submission object."""
        images = []

        # pull largest "preview" image from submission metadata (gallery image urls)
        urls = [v['s']['u'] for v in submission.media_metadata.values()]

        for count, url in enumerate(urls):
            # number images coming from the same gallery
            submission_name = f'{submission.name}-{count}'
            tup = (submission_name, url)
            images.append(tup)
        return images


    def _compile_submissions(self, submissions):
        images = []
        for submission in submissions:
            if hasattr(submission, 'is_gallery'):
                gallery_images = self._get_gallery_urls(submission)
                images.extend(gallery_images)
            else:
                tup = (submission.name, submission.url)
                images.append(tup)
        return images

    def save_pics_to(self, submissions: list, save_dir: str=os.path.join('.', 'images')):
        """Save submission images to file system."""
        make_dir_if_not_exist(save_dir)
        image_subs = self._compile_submissions(submissions)


        # multithread all the picture requests for faster retrieval
        with ThreadPoolExecutor(6) as executor:
            images = [executor.submit(get_image_from_url, url) for name, url in image_subs]
            # process and save images

            for i in range(len(image_subs)):
                name, url = image_subs[i]
                image = images[i].result()
                extension = self._regex_image_exts.search(url)
                filename =  extension.group(0)
                save_image(save_dir, image, name, filename)

        if self._logging:
            print(f'Save complete.  All images located at {save_dir}')
