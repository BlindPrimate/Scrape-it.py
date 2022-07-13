Scrape-it.py
-----------

Scrape-it.py is a small python script which will scrape all images from the current top posts on a target subreddit, and save them to a designated directory.

The script now relies on PRAW to pull from the reddit API rather than scraping from reddit directly.

#### Use


Currently, the only required argument is the target subreddit.( -s )   A target download direcotry can also be designated. ( -d ) If no target directory is given the images will be downloaded to the current working direcotry.  

##### Examples

>$ python scrape-it.py -s aww -d /users/JohnDoe/reddit-images/

Result: All images from /r/aww subreddit will be saved in the directory '/users/JohnDoe/reddit-images/

>$ python scrape-it.py -s funny

Result:  All images from /r/funny subreddit will be save in the current working directory.


#### Dependencies

* Requests
* praw

