import os
import yaml
from scraper import Scraper


CONFIG_PATH = os.path.join(".", "configuration")


with open(os.path.join(CONFIG_PATH, "praw_config.yml"), "r") as f:
    CONFIG = yaml.safe_load(f)



if __name__ == '__main__':
    import argparse
    import os

    # builds command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', type=str, dest='root_directory',
                        default=os.getcwd(), help='Designate desination direcotry for images')
    parser.add_argument('-s', '--subreddit', type=str, dest='subreddit', required=True,
                        help='Designate target subreddit')

    args = parser.parse_args()

    # formats direcotry string to ensure it ends with '/'
    if not args.root_directory.endswith('/'):
        args.root_directory += '/'


    reddit_scraper = Scraper(CONFIG, args.subreddit)

    # reddit_scraper.save_top_pics(args.subreddit, args.root_directory)


