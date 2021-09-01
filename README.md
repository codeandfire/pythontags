This dataset contains the tagging data of 1.75 million Python-related questions on StackOverflow.

Each line in this dataset is a comma-separated list of tags given to a question that has been tagged as 'python' on StackOverflow. There are 1.75 million lines, corresponding to the same number of questions.

To get some basic intuition on this dataset, check [this](exploration/index.md) out.

### Collection

This dataset was scraped from the [StackOverflow site](https://www.stackoverflow.com) on 14-15 August, 2021 using the Python script `scraper.py`. It took about 22 hours to complete.

### Details

To run `scraper.py`, you will need to
```
$ pip install beautifulsoup4 requests tqdm
```
and then
```
$ python3 scraper.py
```

Basically, this script looks up the link <https://www.stackoverflow.com/questions/tagged/python>, which lists questions that have been tagged with the tag 'python'. As of August 15, 2021, this link says that there are 118422 pages of results, and if you change the number of results per page from the default of 15 to the maximum of 50, it turns out that there are 35527 pages. This dataset has been scraped by specifying
```
$ python3 scraper.py --num-pages 35000
```
i.e., scrape the first 35000 pages of results, which yields 35000 x 50 = 1.75 million results in total.

One page of search results is scraped at a time. I found that trying to scrape several pages in parallel tends to get the scraper blocked.

Another point is that the pages are scraped in reverse order. In other words, if you specify say 35000 pages to be scraped, the script starts scraping with the 35000th page, followed by the 34999th, the 34998th and finally ending with the 1st page. Why? The reason goes as follows. By default, StackOverflow presents results in the order of newest questions first, and new questions arrive in StackOverflow by the minute. Due to this, it turns out that when we are scraping some n-th page, by the time we finish scraping that page, if some new questions arrive in StackOverflow, what happens is that some results on the n-th page move to the (n+1)-th page, and then when we scrape the (n+1)-th page, we end up scraping some questions which we have already scraped before. And you can imagine that over say 35000 pages - which can take several hours to scrape - the number of double-counted questions can grow quite large. Scraping pages in reverse order resolves this problem: while scraping the n-th page, even if some new questions arrive, we won't be double-counting any questions when we move to the (n-1)-th page.

(StackOverflow doesn't provide an option to present results in the order of oldest first, or in any other order that guarantees the uniqueness of results even as new questions arrive.)

As is the case with every scraper, a key issue to watch out for in this script is to avoid getting blocked by StackOverflow. This script has two options to prevent that from happening:
  1. Pause the scraper from time to time. By default, the script is configured to pause the scraper for 1 minute after every 100 pages. This default setting works quite well in practice.
  2. Authenticate into StackOverflow. If you have a StackOverflow account, provide your email and password to the script and it will login into StackOverflow. This might help to prevent blocking, though I think the first option is more effective.

If the scraper does get blocked, this script has a setting to halt the scraper for some time before retrying. By default, the scraper is halted for 10 minutes.

Errors encountered while querying StackOverflow are recorded in a log file `scraper.log`. You can look up this log file to find out if the scraper got blocked or faced any other problems.

The scraper's default settings can be changed. A full list of options is presented below:
```
$ python3 scraper.py --help
usage: scraper.py [-h] [--num-pages NUM_PAGES] [--email EMAIL]
                  [--password PASSWORD] [--pause-after PAUSE_AFTER]
                  [--pause PAUSE] [--halt HALT] [--output-file OUTPUT_FILE]
                  [--write-after WRITE_AFTER]
                  [--questions-tab {newest,active,bountied,unanswered,frequent,votes}]
                  [--no-reverse] [--pagesize {15,30,50}]

A script to scrape the tags of questions tagged as 'python' on StackOverflow.

optional arguments:
  -h, --help            show this help message and exit
  --num-pages NUM_PAGES
                        number of pages to scrape (default: 1000)
  --email EMAIL         email for login into stackoverflow (default: None)
  --password PASSWORD   password for login into stackoverflow (default: None)
  --pause-after PAUSE_AFTER
                        pause after every PAUSE_AFTER pages to avoid being
                        blocked (default: 100)
  --pause PAUSE         pause for PAUSE number of seconds after every
                        PAUSE_AFTER pages to avoid being blocked (default: 60)
  --halt HALT           halt for HALT number of seconds before retrying after
                        detecting that the scraper is blocked (default: 600)
  --output-file OUTPUT_FILE
                        file to write the scraped output to (default:
                        dataset.csv)
  --write-after WRITE_AFTER
                        write data to OUTPUT_FILE after every WRITE_AFTER
                        pages (default: 50)
  --questions-tab {newest,active,bountied,unanswered,frequent,votes}
                        questions tab specified to stackoverflow (default:
                        newest)
  --no-reverse          scrape pages in normal order instead of reverse order
                        (default: False)
  --pagesize {15,30,50}
                        pagesize specified to stackoverflow (default: 50)
```
