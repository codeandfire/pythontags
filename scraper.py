"""A script to scrape the tags of questions tagged as 'python' on StackOverflow."""

import argparse
import logging
import time

from bs4 import BeautifulSoup
import requests
from tqdm import tqdm


# arguments
# ---------

parser = argparse.ArgumentParser(
    description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    '--num-pages', type=int, default=1000,
    help='number of pages to scrape'
)
parser.add_argument(
    '--email', type=str, default=None,
    help='email for login into stackoverflow'
)
parser.add_argument(
    '--password', type=str, default=None,
    help='password for login into stackoverflow'
)
parser.add_argument(
    '--pause-after', type=int, default=100,
    help='pause after every PAUSE_AFTER pages to avoid being blocked'
)
parser.add_argument(
    '--pause', type=int, default=60,
    help='pause for PAUSE number of seconds after every PAUSE_AFTER pages to avoid being blocked'
)
parser.add_argument(
    '--halt', type=int, default=600,
    help='halt for HALT number of seconds before retrying after detecting that the scraper is blocked'
)
parser.add_argument(
    '--output-file', type=str, default='dataset.csv',
    help='file to write the scraped output to'
)
parser.add_argument(
    '--write-after', type=int, default=50,
    help='write data to OUTPUT_FILE after every WRITE_AFTER pages'
)
parser.add_argument(
    '--questions-tab', type=str, default='newest',
    choices=['newest', 'active', 'bountied', 'unanswered', 'frequent', 'votes'],
    help='questions tab specified to stackoverflow'
)
parser.add_argument(
    '--no-reverse', action='store_true',
    help='scrape pages in normal order instead of reverse order\n'
)
parser.add_argument(
    '--pagesize', type=str, default='50',
    choices=['15', '30', '50'],
    help='pagesize specified to stackoverflow'
)
args = parser.parse_args()


# set up log file
logging.basicConfig(filename='scraper.log', filemode='w', level=logging.WARNING)


# scraping
# --------

# using a session uses less time per connection
session = requests.Session()

# authenticate into stackoverflow if email and password are provided
if args.email is not None and args.password is not None:
    session.post(
        'https://stackoverflow.com/users/login?ssrc=head&returnurl=https%3a%2f%2fstackoverflow.com%2f',
        data = {
            'email': args.email,
            'password': args.password
        }
    )

# parameters to pass to every GET request
params = {
    'tab': args.questions_tab,
    'pagesize': args.pagesize
}

tags_list = []
mode = 'w'

if args.no_reverse:
    page_iterator = range(1, args.num_pages+1)
else:
    page_iterator = range(args.num_pages, 0, -1)

# tqdm adds a progress bar
page_iterator = tqdm(page_iterator, desc='scraping', unit='page')

for page in page_iterator:

    # page 1 should have no page parameter
    if page > 1:
        params['page'] = str(page)

    while True:

        # query stackoverflow
        response = session.get(
            'https://www.stackoverflow.com/questions/tagged/python',
            params=params
        )

        if response.status_code == 200:   # all ok
            break
        elif response.status_code == 429: # blocked
            logging.warning(
                f'page {page}: scraper blocked, halting ...'
            )
            time.sleep(args.halt)
        else:                             # something else wrong
            logging.warning(
                f'page {page}: status code of {response.status_code} received, retrying ...'
            )

    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    # a simple analysis of the HTML reveals that the "tags" are contained in
    # a-tags of the form <a class='post-tag'>...</a> present within div-tags
    # of the form <div class='question-summary'>...</div>
    for question_div in soup.find_all('div', 'question-summary'):

        tags = []
        for a in question_div.find_all('a', 'post-tag'):
            tag_name = a.string

            # sometimes a.string doesn't contain the text of the "tag"
            if tag_name is None:
                tag_name = a.contents[1]

            # skip the "tag" with text 'python'
            elif tag_name == 'python':
                continue

            tags.append(tag_name)

        tags_list.append(tags)

    first_page = (page == 1) if args.no_reverse else page == args.num_pages
    last_page = (page == args.num_pages) if args.no_reverse else page == 1

    # write the scraped tags to file
    if not first_page and (page % args.write_after == 0 or last_page):

        # separate tags of a single question with commas
        tags_data = '\n'.join([','.join(tags) for tags in tags_list])

        with open(args.output_file, mode) as f:
            f.write(tags_data)
            f.write('\n')

        tags_list = []

        # initially the mode to write to the output file was 'w' (write),
        # henceforth it should be 'a' (append)
        mode = 'a'

    # regular pausing to avoid blocking
    if not (first_page or last_page) and (page_num % args.pause_after == 0):
        time.sleep(args.pause)

session.close()
