
import sys
from scaper import Scraper





def return_links(page):
    # pulls html text from page 
    page = requests.get(page)

    if page.status_code == 200:

        page = html.fromstring(page.text)

        urls = page.xpath('//a/@href')
        return urls
    else:
        print('Bad response from server.')
        sys.exit()



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


    reddit_scraper = Scraper(args.subreddit)

    reddit_scraper.save_top_pics(args.subreddit, args.root_directory)


