## Part 1

### Number of Tags

Let us look at the number of blank lines in the dataset. As we mentioned earlier, this gives the number of questions that were tagged only as 'python'.
```bash
$ grep -c '^$' dataset.csv
```
```
113606
```
Then let us see the number of lines containing only one tag. These correspond to questions that were given only one tag other than 'python'.
```bash
$ grep -E -c '^[^,]+$' dataset.csv
```
```
432795
```
Some examples of such lines (questions) are
```bash
$ grep -E -m 10 '^[^,]+$' dataset.csv
```
```
tkinter
metadata
sqlalchemy
macos
httplib
ruby
scons
import
urllib2
lamp
```
Similarly let us look at questions given two tags (other than 'python') ...
```bash
$ grep -E -m 10 '^[^,]+,[^,]+$' dataset.csv 
```
```
postgresql,psycopg2
pagination,couchdb
macos,textmate
constants,language-construct
pylons,mako
multithreading,multicore
python-3.x,tkinter
unicode,decode
django,localization
django,django-templates
```
```bash
$ grep -E -c '^[^,]+,[^,]+$' dataset.csv
```
```
535465
```
... three tags:
```bash
$ grep -E -m 10 '^([^,]+,){2}[^,]+$' dataset.csv
```
```
com,itunes,py2exe
unit-testing,module,packages
image,wxpython,image-manipulation
ruby,django,haml
ssl,openssl,m2crypto
html,css,cgi
django,django-admin,django-urls
java,ruby,multithreading
debugging,google-app-engine,jinja2
ruby,path,module
```
```bash
$ grep -E -c '^([^,]+,){2}[^,]+$' dataset.csv
```
```
388217
```
... four tags:
```bash
$ grep -E -m 10 '^([^,]+,){3}[^,]+$' dataset.csv
```
```
file,datetime,date,calendar
unix,passwords,fabric,passwd
math,substitution,symbolic-math,sympy
django,content-type,django-orm,django-comments
java,php,email,parsing
clojure,smtp,imap,pop3
json,xml,google-app-engine,configuration-files
django,aes,portability,pycrypto
linux,shell,command-line,console
decorator,default-value,class-method,static-methods
```
```bash
$ grep -E -c '^([^,]+,){3}[^,]+$' dataset.csv
```
```
279908
```
... and five tags:
```bash
$ grep -E -c '^([^,]+,){4}[^,]+$' dataset.csv
```
```
9
```
```bash
$ grep -E '^([^,]+,){4}[^,]+$' dataset.csv
```
```
windows,matlab,matlab-deployment,python-mlab,mlab
php,post,request,forms,http-post
matlab,win32com,pythoncom,python-mlab,mlab
jquery,firefox,multipartform-data,forms,http-post
file-upload,flask,error-handling,forms,http-post
ajax,button,flask,forms,http-post
api,flask,submit,forms,http-post
html,django,django-forms,forms,http-post
django,csv,httpresponse,forms,http-post
```
There are no questions with six tags or more:
```bash
$ grep -E -c '^([^,]+,){5,}[^,]+$' dataset.csv 
```
```
0
```

### Tag Frequency

Now let us examine the individual tags more closely. Let us look at the entire set of tags along with their frequency, i.e. the number of times they occur in the dataset.
```bash
$ tr ',' "\n" < dataset.csv | tr -s "\n" | sort | uniq -c | sort -nr > tags_freq.txt
```
The most frequent tags are ...
```bash
$ head tags_freq.txt
```
```
 181575 pandas
 173536 python-3.x
 134516 django
  81999 numpy
  62509 python-2.7
  59240 dataframe
  56425 list
  50954 matplotlib
  40151 tensorflow
  38067 dictionary
```
... and some of the least frequent tags are:
```bash
$ tail tags_freq.txt
```
```
      1 3d-texture
      1 3dcamera
      1 37-signals
      1 360-virtual-reality
      1 32feet
      1 3270
      1 2phase-commit
      1 2-legged
      1 2dsphere
      1 21cfr11
```
Let us see the total number of unique tags in this dataset:
```bash
$ wc -l tags_freq.txt 
```
```
24806 tags_freq.txt
```
That's a lot of tags!

Let us have a look at the number of very, very rare tags, i.e. they occur only once in the entire dataset.
```bash
$ grep -E -c '^[[:space:]]+1[[:space:]]' tags_freq.txt
```
```
6048
```
Quite a large number of tags occur only once. Consider tags that occur only twice ...
```bash
$ grep -E -m 10 '^[[:space:]]+2[[:space:]]' tags_freq.txt
```
```
      2 zune
      2 zulip
      2 zopeskel
      2 zkteco
      2 zipper
      2 zinnia-entry
      2 zingchart
      2 zigzag-encoding
      2 zfs
      2 zero-copy
```
```bash
$ grep -E -c '^[[:space:]]+2[[:space:]]' tags_freq.txt
```
```
2756
```
... or rather the total number of tags that occur less than 10 times:
```bash
$ grep -E -c '^[[:space:]]+[[:digit:]][[:space:]]' tags_freq.txt
```
```
15247
```
Similarly, consider tags that occur at least 10 but less than 100 times ...
```bash
$ grep -E -c '^[[:space:]]+[[:digit:]]{2}[[:space:]]' tags_freq.txt
```
```
6779
```
... with examples:
```bash
$ grep -E -m 10 '^[[:space:]]+9[[:digit:]][[:space:]]' tags_freq.txt
```
```
     99 worker
     99 wlst
     99 sonarqube
     99 simplify
     99 separator
     99 qwebview
     99 qscrollarea
     99 lasso-regression
     99 inner-classes
     99 google-authentication
```
```bash
$ grep -E -m 10 '^[[:space:]]+8[[:digit:]][[:space:]]' tags_freq.txt
```
```
     89 vision
     89 url-for
     89 urlfetch
     89 taskscheduler
     89 subdomain
     89 server-sent-events
     89 removing-whitespace
     89 profiler
     89 named-pipes
     89 microphone
```
```bash
$ grep -E -m 10 '^[[:space:]]+7[[:digit:]][[:space:]]' tags_freq.txt
```
```
     79 visual-studio-2019
     79 string-interpolation
     79 stl
     79 static-typing
     79 stack-overflow
     79 spring
     79 sitemap
     79 shlex
     79 serial-communication
     79 opengl-compat
```
```bash
$ grep -E -m 10 '^[[:space:]]+6[[:digit:]][[:space:]]' tags_freq.txt
```
```
     69 webfaction
     69 tcp-ip
     69 sybase
     69 squish
     69 solaris
     69 sigint
     69 rx-py
     69 pyuic
     69 pytesser
     69 portfolio
```
```bash
$ grep -E -m 10 '^[[:space:]]+5[[:digit:]][[:space:]]' tags_freq.txt
```
```
     59 url-redirection
     59 theano-cuda
     59 surf
     59 statements
     59 shared-hosting
     59 sframe
     59 quaternions
     59 qlayout
     59 pywikibot
     59 pyvirtualdisplay
```
```bash
$ grep -E -m 10 '^[[:space:]]+4[[:digit:]][[:space:]]' tags_freq.txt
```
```
     49 xdist
     49 unix-socket
     49 turbogears
     49 tsv
     49 trendline
     49 tile
     49 three.js
     49 tf.data.dataset
     49 tabulate
     49 sql-delete
```
```bash
$ grep -E -m 10 '^[[:space:]]+3[[:digit:]][[:space:]]' tags_freq.txt
```
```
     39 wxformbuilder
     39 week-number
     39 virtualization
     39 vcf-vcard
     39 user-profile
     39 trimesh
     39 toggle
     39 timeoutexception
     39 timeline
     39 tab-delimited-text
```
```bash
$ grep -E -m 10 '^[[:space:]]+2[[:digit:]][[:space:]]' tags_freq.txt
```
```
     29 zerorpc
     29 xlsm
     29 windows-server-2008
     29 weighted-graph
     29 webbrowser-control
     29 vowpalwabbit
     29 vimeo
     29 vcf-variant-call-format
     29 vbo
     29 user-registration
```
```bash
$ grep -E -m 10 '^[[:space:]]+1[[:digit:]][[:space:]]' tags_freq.txt
```
```
     19 yql
     19 wsh
     19 windows-shell
     19 webhdfs
     19 watson-conversation
     19 wampserver
     19 vscode-extensions
     19 vm-implementation
     19 vizard
     19 u-sql
```
... and tags that occur at least 100 but less than 1000 times:
```bash
$ grep -E -c '^[[:space:]]+[[:digit:]]{3}[[:space:]]' tags_freq.txt
```
```
2295
```
```bash
$ grep -E -m 10 '^[[:space:]]+9[[:digit:]]{2}[[:space:]]' tags_freq.txt
```
```
    999 type-hinting
    999 boost
    994 pyautogui
    989 memory-management
    987 python-2.6
    986 jenkins
    984 firebase
    983 webdriverwait
    982 soap
    979 mypy
```
```bash
$ grep -E -m 10 '^[[:space:]]+8[[:digit:]]{2}[[:space:]]' tags_freq.txt
```
```
    899 extract
    899 bigdata
    896 nonetype
    896 nested-loops
    895 glob
    893 vba
    890 windows-10
    889 ironpython
    886 telegram-bot
    885 reactjs
```
```bash
$ grep -E -m 10 '^[[:space:]]+7[[:digit:]]{2}[[:space:]]' tags_freq.txt
```
```
    797 reshape
    797 outlook
    792 neo4j
    791 jupyter-lab
    788 boost-python
    783 try-catch
    781 latex
    781 command-line-interface
    780 graphics
    780 blender
```
```bash
$ grep -E -m 10 '^[[:space:]]+6[[:digit:]]{2}[[:space:]]' tags_freq.txt
```
```
    697 eval
    696 google-sheets
    694 compilation
    693 parameter-passing
    692 protocol-buffers
    692 aggregate
    687 loss-function
    686 mean
    686 filtering
    685 pyglet
```
```bash
$ grep -E -m 10 '^[[:space:]]+5[[:digit:]]{2}[[:space:]]' tags_freq.txt
```
```
    597 colorbar
    596 webserver
    596 wagtail
    595 self
    594 linear-programming
    593 row
    592 matrix-multiplication
    591 graph-theory
    591 dictionary-comprehension
    589 try-except
```
```bash
$ grep -E -m 10 '^[[:space:]]+4[[:digit:]]{2}[[:space:]]' tags_freq.txt
```
```
    499 png
    499 min
    499 imaplib
    499 dependencies
    499 configparser
    498 text-mining
    498 django-channels
    497 packaging
    497 docstring
    496 grid-search
```
```bash
$ grep -E -m 10 '^[[:space:]]+3[[:digit:]]{2}[[:space:]]' tags_freq.txt
```
```
    399 sage
    399 index-error
    398 pymssql
    398 client-server
    398 appium
    397 null
    397 multiplication
    397 amazon-redshift
    396 marshmallow
    396 grpc
```
```bash
$ grep -E -m 10 '^[[:space:]]+2[[:digit:]]{2}[[:space:]]' tags_freq.txt
```
```
    299 swift
    299 ruby-on-rails
    299 keyword
    299 event-handling
    298 symbolic-math
    298 pyopenssl
    298 powerpoint
    298 postgis
    298 libraries
    298 blob
```
```bash
$ grep -E -m 10 '^[[:space:]]+1[[:digit:]]{2}[[:space:]]' tags_freq.txt
```
```
    199 stored-procedures
    199 rasa-nlu
    199 pypyodbc
    199 formset
    199 anaconda3
    198 torchvision
    198 schema
    198 qpushbutton
    198 point-clouds
    198 overwrite
```
... and tags that occur at least 1000 but less than 10000 times:
```bash
$ grep -E -c '^[[:space:]]+[[:digit:]]{4}[[:space:]]' tags_freq.txt
```
```
432
```
```bash
$ grep -E -m 30 '^[[:space:]]+[[:digit:]]{4}[[:space:]]' tags_freq.txt
```
```
   9859 django-rest-framework
   9745 pyqt5
   9684 multiprocessing
   9681 selenium-webdriver
   9557 sql
   9466 plot
   9389 pycharm
   9291 macos
   9210 subprocess
   9118 c++
   9099 sockets
   9067 anaconda
   8854 kivy
   8704 amazon-web-services
   8683 image-processing
   8667 sorting
   8412 image
   8124 parsing
   8095 apache-spark
   8028 performance
   7953 discord.py
   7725 api
   7495 database
   7299 nlp
   7257 if-statement
   7219 pytorch
   7212 neural-network
   7121 django-views
   7010 mongodb
   6992 recursion
```
Finally, the most frequent tags, that occur at least 10000 times:
```bash
$ grep -E '^[[:space:]]+[[:digit:]]{5,}[[:space:]]' tags_freq.txt
```
```
 181575 pandas
 173536 python-3.x
 134516 django
  81999 numpy
  62509 python-2.7
  59240 dataframe
  56425 list
  50954 matplotlib
  40151 tensorflow
  38067 dictionary
  35657 flask
  35010 tkinter
  31494 regex
  28411 selenium
  27948 arrays
  27641 csv
  26724 json
  26406 string
  22431 html
  22411 keras
  22232 beautifulsoup
  21598 machine-learning
  21533 opencv
  21072 web-scraping
  18412 scikit-learn
  15970 scipy
  15688 mysql
  15458 loops
  15340 function
  15180 javascript
  15060 sqlalchemy
  15016 pip
  14795 pygame
  14509 python-requests
  14243 django-models
  13783 multithreading
  13743 linux
  13687 datetime
  13427 for-loop
  13081 windows
  12865 class
  12640 pyqt
  11688 scrapy
  11255 excel
  11142 google-app-engine
  10808 algorithm
  10728 jupyter-notebook
  10487 file
  10376 pyspark
  10276 xml
  10137 deep-learning
  10106 sqlite
  10056 postgresql
```

---

For more, proceed to [Part 2](part-2.md).
