Reddit Media Scraper
-----------

Scrape-it.py is a small python script which will scrape all images from the current top posts on a target subreddit, and save them to a designated directory.

The script now relies on PRAW to pull from the reddit API rather than scraping from reddit directly.


#### Installation

The code can be run as either a module or standalone script.

If running as a script, it is recommended that the script be run inside a pipenv environment.  Install pipenv [https://pipenv.pypa.io/en/latest/install/](https://pipenv.pypa.io/en/latest/install/)


After install run the following:
> $ pipenv install

To access the pipenv:
> $ pipenv shell

The reddit API requires an API ID and key be used.  To set these, use the file located at configuration/praw_config-sample.yml.  Fill in the details requested in the file.  A reddit API key can be acquired following these instructions:  [https://www.reddit.com/wiki/api](https://www.reddit.com/wiki/api).  Once the information is entered, rename the file to remove '-sample' from the name.


#### Use

Currently, the only required argument is the target subreddit.( -s )   A target download direcotry can also be designated. ( -d ) If no target directory is given the images will be downloaded to the current working direcotry.  

##### Examples

>$ python . -s aww -d /users/JohnDoe/reddit-images/

Result: All images from /r/aww subreddit will be saved in the directory '/users/JohnDoe/reddit-images/

>$ python . -s funny

Result:  All images from /r/funny subreddit will be save in the current working directory.


#### Dependencies

* Requests
* praw

