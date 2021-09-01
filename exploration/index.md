## Exploring the Dataset

This note describes some basic exploration that you can do with the `pythontags` dataset in order to get familiar with it.

This note is divided into two parts: [Part 1](part-1.md) and [Part 2](part-2.md).

For this "exploration", we use a Bash shell with some basic programs like `head`, `tail`, `grep` and `wc`. On Windows, you can use Git Bash.

For starters, let us look at the first few entries of this dataset ...
```bash
$ head dataset.csv
```
```
postgresql,psycopg2
com,itunes,py2exe

tkinter
pagination,couchdb
macos,textmate

constants,language-construct
metadata

```
... and the last few entries.
```bash
$ tail dataset.csv
```
```
json,combinations,itertools
proxy,scrapy
pandas,dataframe
module,playsound

nlp
regex
tensorflow
python-3.x,algorithm,time-complexity
amazon-web-services,amazon-s3,amazon-rekognition
```
As you can see, this dataset contains lines of comma-separated tags, each line corresponding to a question tagged as 'python' in the StackOverflow database. There are also some blank lines: these correspond to questions that were given no tag other than 'python'.

Let us see the total number of lines in this dataset:
```bash
$ wc -l dataset.csv 
```
```
1750000 dataset.csv
```
Indeed, we have 1.75 million lines, corresponding to 1.75 million questions in StackOverflow.

Let us look at the total number of individual tags in this dataset:
```bash
$ tr ',' ' ' < dataset.csv | wc -w
```
```
3788053
```
i.e. approximately 3.79 million.

With that, let us proceed to [Part 1](part-1.md).
