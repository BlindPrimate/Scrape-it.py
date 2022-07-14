from scraper import *




if __name__ == '__main__':
    import os
    import argparse
    import yaml

    CONFIG_PATH = os.path.join(".", "configuration")

    with open(os.path.join(CONFIG_PATH, "praw_config.yml"), "r") as f:
        CONFIG = yaml.safe_load(f)

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


    reddit_scraper = Scraper(CONFIG, args.subreddit, logging=True)

    top = reddit_scraper.get_top_image_submissions('week')
    reddit_scraper.save_pics_to(top)




