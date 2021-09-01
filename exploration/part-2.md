## Part 2

### Tag Sequences

In the previous part we looked at frequent tags, but we only considered individual tags. What about tag sequences, as in, the whole sequence of tags used to "tag" a question? Can we find sequences that are more frequent than others?
```bash
$ sort dataset.csv | uniq -c | sort -nr | head -n 20
```
```
 113606 
  44545 pandas
  30387 python-3.x
  27679 django
  18804 pandas,dataframe
  13223 regex
  11343 numpy
  11169 matplotlib
  10533 python-2.7
   9454 tkinter
   8859 list
   6908 dictionary
   6401 tensorflow
   5219 arrays,numpy
   5211 pygame
   4566 csv
   4504 json
   4427 flask
   4115 selenium
   3910 beautifulsoup
```
At the top of this list we have the number '113606' apparently followed by nothing. This "nothing" actually stands for the blank lines in our dataset: the most common tag "sequence" is just the lone tag 'python'.

As you can see this mostly identifies individual tags. In order to focus solely on tag sequences of length greater than 1, we will slightly alter the previous command:
```bash
$ grep ',' dataset.csv | sort | uniq -c | sort -nr > seqs_freq.txt
$ head -n 100 seqs_freq.txt
```
```
  18804 pandas,dataframe
   5219 arrays,numpy
   3600 python-3.x,pandas
   3467 pandas,numpy
   3443 django,django-rest-framework
   3427 django,django-models
   3088 tensorflow,keras
   2357 web-scraping,beautifulsoup
   2337 pandas,matplotlib
   2334 list,dictionary
   2139 python-3.x,tkinter
   2066 python-3.x,pandas,dataframe
   1746 pandas,pandas-groupby
   1700 discord,discord.py
   1683 python-3.x,list
   1624 pandas,csv
   1499 matplotlib,plot
   1487 selenium,selenium-webdriver
   1419 python-3.x,dictionary
   1404 apache-spark,pyspark
   1400 html,django
   1358 pandas,datetime
   1330 python-2.7,python-3.x
   1283 numpy,scipy
   1269 django,django-forms
   1263 numpy,matplotlib
   1186 django,django-templates
   1152 mongodb,pymongo
   1148 regex,python-3.x
   1140 python-3.x,python-2.7
   1138 excel,pandas
   1030 django,django-admin
   1013 user-interface,tkinter
   1005 mysql,django
   1003 string,list
   1001 matplotlib,seaborn
    991 machine-learning,scikit-learn
    984 pandas,numpy,dataframe
    978 python-3.x,pygame
    969 html,beautifulsoup
    956 regex,string
    938 web-scraping,scrapy
    937 pyqt,pyqt5
    927 django,django-views
    917 python-3.x,numpy
    812 opencv,image-processing
    806 django,python-3.x
    792 django,postgresql
    778 regex,pandas
    775 selenium,web-scraping
    770 python-3.x,matplotlib
    761 django,forms
    759 numpy,pandas
    751 pandas,dataframe,pandas-groupby
    748 json,pandas
    713 django,django-queryset
    698 list,tuples
    692 json,python-3.x
    687 csv,pandas
    672 excel,openpyxl
    671 regex,python-2.7
    667 html,flask
    661 python-2.7,pandas
    642 flask,jinja2
    631 numpy,matrix
    623 postgresql,sqlalchemy
    620 tensorflow,machine-learning,keras,deep-learning
    604 python-3.x,csv
    599 django,django-models,django-forms
    594 html,web-scraping,beautifulsoup
    591 kivy,kivy-language
    586 python-3.x,discord,discord.py
    586 json,dictionary
    579 list,sorting
    572 xml,elementtree
    561 apache-spark,pyspark,apache-spark-sql
    560 django,heroku
    555 postgresql,psycopg2
    547 pandas,dictionary
    544 twitter,tweepy
    542 pandas,group-by
    539 django,django-models,django-views
    529 python-3.x,beautifulsoup
    520 sqlalchemy,flask-sqlalchemy
    518 python-2.7,tkinter
    517 pandas,scikit-learn
    504 tensorflow,keras,deep-learning
    498 tensorflow,deep-learning
    497 pandas,time-series
    495 pandas,matplotlib,seaborn
    493 google-app-engine,google-cloud-datastore
    491 python-2.7,dictionary
    484 arrays,list
    480 selenium,selenium-chromedriver
    478 list,list-comprehension
    473 python-3.x,python-requests
    473 django,celery
    471 mysql,sqlalchemy
    469 list,python-3.x
    468 python-3.x,pyqt,pyqt5
```
Note that these sequences are order-sensitive, i.e. a sequence 'pandas,dataframe' refers to a question tagged exactly as 'pandas' followed by 'dataframe', and not 'dataframe,pandas'.

The total number of unique tag sequences in the dataset is
```bash
$ wc -l seqs_freq.txt 
572266 seqs_freq.txt
```
Next let us look at some of the rare tag sequences, that occur only once ...
```bash
$ tail seqs_freq.txt 
      1 2d,curve-fitting,gaussian
      1 2d,coordinates,game-development
      1 2d,coordinates
      1 2d,colormap,color-mapping
      1 2d,collision-detection,collision
      1 2d,collision
      1 2d,cairo,pycairo
      1 2d,auto-generate,terrain
      1 2d,ascii
      1 2d,antialiasing
```
... and the total number of such sequences is:
```bash
$ grep -E -c '^[[:space:]]+1[[:space:]]' seqs_freq.txt 
481231
```

### Co-occurring Tags

Now, let us examine the tags in a different way. For a given tag, suppose we want to find out the tags that it most frequently co-occurs with.

Consider the tag 'pandas'. To just get an idea of the kinds of tags that surround the given tag, we can simply look at a sample of lines from the dataset containing that tag:

```bash
$ tag='pandas'
$ pattern="^$tag,|,$tag,|,$tag$|^$tag$"
$ grep -E -m 30 "$pattern" dataset.csv
```
```
finance,quantitative-finance,pandas
list-comprehension,time-series,pandas
sorting,numpy,pandas
statistics,correlation,pandas
r,numpy,pandas,data.table
pandas
numpy,pandas
pandas,performance,dataframe,for-loop
compiler-errors,installation,pandas
pandas
pandas
csv,numpy,tab-delimited,pandas
csv,numpy,tab-delimited,pandas
dataframe,panels,pandas
pandas,numpy,python-2.6
r,join,data.table,pandas
io,pandas
transform,dataframe,pandas
numpy,pandas
python-2.7,pivot-table,pandas
numpy,scipy,enthought,pandas
dataframe,pandas
pandas,dataframe,pivot-table
pandas
numpy,pandas
hdf5,pandas
pandas,csv
pandas
parsing,datetime,pandas
pandas,fixed-width
```
Then we can get the most frequent co-occurring tags with their counts as:
```bash
$ grep -E "$pattern" dataset.csv | tr ',' "\n" | sort | uniq -c | sort -nr | head -n 20
```
```
 181575 pandas
  51248 dataframe
  13923 numpy
  13487 python-3.x
   7707 matplotlib
   7388 csv
   5513 datetime
   5304 pandas-groupby
   3593 excel
   2954 dictionary
   2607 group-by
   2596 python-2.7
   2477 list
   2463 json
   2342 scikit-learn
   2270 merge
   2051 time-series
   2051 string
   1928 seaborn
   1922 regex
```
Of course 'pandas' will always co-occur with 'pandas', so you can ignore the first entry of this list, but the others are quite informative: for example 'dataframe' co-occurs with 'pandas' 51248 times, 'numpy' co-occurs with 'pandas' 13923 times and so on.

In a similar fashion let us look at some other tags. Take 'django' next ...
```bash
$ tag='django'
$ pattern="^$tag,|,$tag,|,$tag$|^$tag$"
$ grep -E -m 30 "$pattern" dataset.csv 
```
```
django,localization
django,content-type,django-orm,django-comments
django,django-templates
ruby,django,haml
django,django-admin,django-urls
django
django,aes,portability,pycrypto
django,navigation
django,aes,pycrypto
django,chat,django-views,livechat
django,apache-flex
django,django-queryset
mysql,django,unit-testing
django,generics,metadata,models
django
django,unicode
django,django-models
django
django,iis,datetime,django-models
django,django-models,django-templates,django-views
django
django,django-forms
django,django-users
django,database-design,django-models,django-admin
django,pickle
django,admin,url
django,templates,ternary-operator
django,django-templates
django,django-models
django
```
```bash
$ grep -E "$pattern" dataset.csv | tr ',' "\n" | sort | uniq -c | sort -nr | head -n 20
```
```
 134516 django
  13774 django-models
   9189 django-rest-framework
   6891 django-views
   5711 django-forms
   5316 python-3.x
   5084 django-templates
   4950 html
   3425 javascript
   3209 django-admin
   3053 postgresql
   2982 mysql
   2522 forms
   2224 django-queryset
   1949 python-2.7
   1949 heroku
   1847 jquery
   1840 json
   1813 celery
   1808 database
```
... then 'numpy':
```bash
$ tag='numpy'
$ pattern="^$tag,|,$tag,|,$tag$|^$tag$"
$ grep -E -m 30 "$pattern" dataset.csv 
```
```
math,audio,numpy,trigonometry
numpy,python-sphinx,restructuredtext
java,numpy,jython,cpython
math,matlab,numpy,scipy
numpy,scipy,spatial,interpolation
numpy
numpy,root,implicit
osx-snow-leopard,numpy,macports
memory-management,numpy,pygame
c++,numpy,scipy
random,numpy
numpy
numpy,pyglet
numpy,scipy,gsl,pygsl
statistics,numpy,machine-learning
macos,numpy,scipy
macos,numpy,matplotlib,scipy
numpy,sparse-matrix
numpy,ctypes
numpy,statistics,matplotlib,scipy
numpy,swig
matlab,numpy,array-broadcasting
numpy,scipy,eigenvalue
numpy,intersection
arrays,numpy,minimum
colors,numpy,python-imaging-library,color-space
numpy,scipy,interpolation
find,numpy
numpy,scipy,sparse-matrix
performance,numpy,line-intersection
```
```bash
$ grep -E "$pattern" dataset.csv | tr ',' "\n" | sort | uniq -c | sort -nr | head -n 20
```
```
  81999 numpy
  15305 arrays
  13923 pandas
   6961 scipy
   5014 python-3.x
   4988 matplotlib
   3234 dataframe
   3048 matrix
   2045 opencv
   1805 python-2.7
   1800 tensorflow
   1692 list
   1674 scikit-learn
   1645 performance
   1534 multidimensional-array
   1496 numpy-ndarray
   1390 vectorization
   1268 machine-learning
   1204 image-processing
   1094 indexing
```
... then 'python-2.7':
```bash
$ tag='python-2.7'
$ pattern="^$tag,|,$tag,|,$tag$|^$tag$"
$ grep -E -m 30 "$pattern" dataset.csv
```
```
python-2.7,mod-python
python-2.7,pyscripter
io,python-2.7
python-2.7
python-2.7,tkinter,python-imaging-library
python-2.7,sockets,networking,socketserver
python-2.7,python-2.6
linux,python-2.7,command-line,os.system
macos,uninstallation,python-2.7
m2crypto,python-2.7,cryptography
openssl,m2crypto,python-2.7
python-2.7,sockets,socketserver
ubuntu,python-2.7,ubuntu-10.04
python-2.7
linux,ubuntu,python-2.7
python-2.7,unicode,utf-8
windows,python-2.7,visual-studio,distutils
database,file,python-2.7,memory
python-2.7,pretty-print,ordereddictionary,pprint
multiprocessing,python-2.7
python-2.7,urllib2,head
python-2.7,syntax,operators,modulo
python-2.7,exception-handling,stack-trace
linux,python-2.7,sockets
opencv,osx-snow-leopard,python-2.7
windows-xp,pygame,python-2.7
python-3.x,python-2.7
scipy,python-2.7
logging,python-2.7
shell,python-2.7
```
```bash
$ grep -E "$pattern" dataset.csv | tr ',' "\n" | sort | uniq -c | sort -nr | head -n 20
```
```
  62509 python-2.7
   7707 python-3.x
   2596 pandas
   2244 list
   1949 django
   1805 numpy
   1769 dictionary
   1461 tkinter
   1396 regex
   1159 csv
   1105 string
   1073 matplotlib
    860 json
    850 pip
    785 beautifulsoup
    739 windows
    678 python-requests
    645 unicode
    644 macos
    625 linux
```
... then 'list':
```bash
$ tag='list'
$ pattern="^$tag,|,$tag,|,$tag$|^$tag$"
$ grep -E -m 30 "$pattern" dataset.csv 
```
```
list,dictionary,error-handling,tuples
list,copy
list,dictionary,reverse
list,sorting,tuples
list,io
list,recursion,tree
string,list
list,beautifulsoup,associative
list
list,sorting,tuples,topological-sort
refactoring,list
refactoring,list
list,blender,cinema-4d
list,sequence
string,list,substitution
string,list,utf-8
list,frequency
list,intersection
list
list,arrays
list
django,json,list,dictionary
list,split
list,dictionary,set
list,instance
string,list,range,ascii
list,sorting,key,genetic-algorithm
list,tuples
list,file
file,list
```
```bash
$ grep -E "$pattern" dataset.csv | tr ',' "\n" | sort | uniq -c | sort -nr | head -n 20
```
```
  56425 list
   8243 python-3.x
   7594 dictionary
   3828 string
   2741 arrays
   2552 tuples
   2477 pandas
   2244 python-2.7
   2177 loops
   2133 for-loop
   1937 sorting
   1692 numpy
   1550 list-comprehension
   1342 dataframe
   1307 function
   1156 append
   1146 indexing
   1036 csv
    762 split
    755 file
```
... then 'tensorflow':
```bash
$ tag='tensorflow'
$ pattern="^$tag,|,$tag,|,$tag$|^$tag$"
$ grep -E -m 30 "$pattern" dataset.csv
```
```
algorithm,tensorflow,machine-learning,keras
tensorflow,neural-network,keras,autoencoder
tensorflow
tensorflow
windows,tensorflow
macos,tensorflow
parallel-processing,deep-learning,tensorflow
installation,pip,tensorflow
docker,anaconda,tensorflow
tensorflow,pip,installation
pip,tensorflow
tensorflow
word2vec,tensorflow
tensorflow,tensor
tensorflow
tensorflow
tensorflow
reshape,tensorflow
anaconda,tensorflow
macos,tensorflow
tensorflow
tensorflow
tensorflow
ubuntu,glibc,tensorflow
tensorflow
gpu,nvidia,tensorflow
logging,tensorflow
import,machine-learning,tensorflow,mnist
tensorflow,tensorboard
tensorflow
```
```bash
$ grep -E "$pattern" dataset.csv | tr ',' "\n" | sort | uniq -c | sort -nr | head -n 20
```
```
  40151 tensorflow
  13661 keras
   5312 machine-learning
   4961 deep-learning
   2798 neural-network
   1800 numpy
   1765 python-3.x
   1625 conv-neural-network
   1485 tensorflow2.0
   1305 lstm
    836 tensorflow-datasets
    630 object-detection
    607 tensorboard
    573 anaconda
    542 tf.keras
    542 gpu
    497 recurrent-neural-network
    480 computer-vision
    475 tensor
    432 google-colaboratory
```
... then 'tkinter':
```bash
$ tag='tkinter'
$ pattern="^$tag,|,$tag,|,$tag$|^$tag$"
$ grep -E -m 30 "$pattern" dataset.csv 
```
```
tkinter
python-3.x,tkinter
tkinter,tkinter.scrollbar
memory,tkinter,python-2.x
binding,tkinter
tkinter,undo-redo
copy,widget,tkinter
lambda,tkinter
tkinter
multithreading,tkinter
tkinter,undo,undo-redo,redo
tkinter,python-2.6,pickle
file-io,tkinter,popen
python-imaging-library,tkinter
tkinter,pickle
memory,tkinter
tkinter
compilation,python-imaging-library,tkinter
tkinter,cursor-position
tkinter,grid,tkinter-entry
tkinter,tooltip
get,settings,widget,tkinter
user-interface,events,tkinter
character-encoding,special-characters,tkinter
windows,tkinter
png,transparency,tkinter
tkinter
tkinter,mouse-position
tkinter,event-binding
tkinter
```
```bash
$ grep -E "$pattern" dataset.csv | tr ',' "\n" | sort | uniq -c | sort -nr | head -n 20
```
```
  35010 tkinter
   5634 python-3.x
   3329 user-interface
   1461 python-2.7
   1165 tkinter-canvas
   1095 button
    888 matplotlib
    869 tk
    813 tkinter-entry
    793 canvas
    694 ttk
    609 multithreading
    570 class
    542 widget
    509 image
    480 label
    447 python-imaging-library
    446 function
    420 treeview
    411 listbox
```
... then 'regex':
```bash
$ tag='regex'
$ pattern="^$tag,|,$tag,|,$tag$|^$tag$"
$ grep -E -m 30 "$pattern" dataset.csv 
```
```
regex
regex
php,sql,regex,perl
regex,string
html,regex
html,regex,parsing
regex
xml,regex,last-occurrence
html,regex,mechanize
regex
regex
regex
regex,unicode,diacritics,unicode-normalization
regex,unicode
regex,string
regex
regex,parsing,lexical-analysis
regex
regex
c#,java,regex,lookbehind
regex,escaping
regex,parsing,grep
regex,string
regex,string
regex
regex
c#,java,php,regex
regex
regex,phone-number
```
```bash
$ grep -E "$pattern" dataset.csv | tr ',' "\n" | sort | uniq -c | sort -nr | head -n 20
```
```
  31494 regex
   2793 python-3.x
   2621 string
   1922 pandas
   1396 python-2.7
    689 parsing
    576 list
    567 beautifulsoup
    563 django
    557 replace
    527 dataframe
    493 split
    484 html
    409 re
    319 regex-group
    295 web-scraping
    293 dictionary
    292 unicode
    287 csv
    284 nlp
```
... then 'selenium':
```bash
$ tag='selenium'
$ pattern="^$tag,|,$tag,|,$tag$|^$tag$"
$ grep -E -m 30 "$pattern" dataset.csv 
```
```
selenium
browser,selenium,selenium-rc
firefox,selenium,offline-mode
selenium
javascript,selenium,screen-scraping
cookies,selenium,selenium-rc
macos,selenium,selenium-rc
ubuntu,selenium
xpath,selenium
unit-testing,selenium
selenium,selenium-rc
selenium,selenium-rc
selenium,selenium-rc
selenium,browser-automation
unit-testing,selenium
selenium,webdriver
internet-explorer,ubuntu,selenium
selenium,selenium-rc,selenium-grid
selenium
selenium
selenium,python-unittest
selenium,selenium-rc
selenium,window,selenium-rc
selenium,webdriver
firefox,selenium,download,firefox-addon
selenium
c#,jquery,selenium,selenium-rc
automation,selenium,webdriver
selenium,selenium-rc
error-handling,selenium,selenium-rc
```
```bash
$ grep -E "$pattern" dataset.csv | tr ',' "\n" | sort | uniq -c | sort -nr | head -n 20
```
```
  28411 selenium
   7338 selenium-webdriver
   3825 web-scraping
   2982 selenium-chromedriver
   2349 python-3.x
   2261 xpath
   1849 webdriver
   1517 html
   1410 beautifulsoup
   1172 javascript
   1071 google-chrome
    947 firefox
    888 webdriverwait
    758 css-selectors
    755 automation
    576 python-2.7
    519 phantomjs
    430 scrapy
    383 geckodriver
    328 web-crawler
```
... then 'opencv':
```bash
$ tag='opencv'
$ pattern="^$tag,|,$tag,|,$tag$|^$tag$"
$ grep -E -m 30 "$pattern" dataset.csv 
```
```
opencv
arrays,matrix,performance,opencv
macos,opencv,macports
opencv,camera,capture
opencv
c,opencv,swig,ctypes
macos,opencv
opencv
opencv,webcam
opencv
c++,opencv,performance
opencv
opencv,macports
opencv,webcam,touchscreen,background-subtraction
opencv,segmentation-fault
opencv
opencv
opencv,xlib
opencv,python-3.x,ctypes
opencv,numpy
image-processing,opencv,machine-learning,barcode-scanner
opencv
opencv
opencv,computer-vision,image-recognition,knn
image,opencv
debugging,memory-leaks,opencv,cpython
image,image-processing,resize,opencv
opencv,blobs
object,opencv,location
opencv
```
```bash
$ grep -E "$pattern" dataset.csv | tr ',' "\n" | sort | uniq -c | sort -nr | head -n 20
```
```
  21533 opencv
   3975 image-processing
   2045 numpy
   2030 computer-vision
   1340 image
   1231 python-3.x
    632 c++
    612 cv2
    487 python-2.7
    464 video
    421 python-imaging-library
    406 opencv3.0
    354 tensorflow
    351 ocr
    340 raspberry-pi
    335 opencv-python
    329 matplotlib
    301 object-detection
    272 scikit-image
    253 machine-learning
```
... then 'loops':
```bash
$ tag='loops'
$ pattern="^$tag,|,$tag,|,$tag$|^$tag$"
$ grep -E -m 30 "$pattern" dataset.csv 
```
```
iterator,loops
loops,beautifulsoup,web-scraping
django,templates,loops
loops,items
django,function,loops
loops,iterator,for-loop
list,sorting,loops,while-loop
loops,nested
variables,loops,naming
list,loops
loops,list
loops,signals,copy-paste,infinity
loops,dictionary
loops,for-loop
loops,raw-input
loops,indexing
loops
loops
sorting,loops
list,loops,for-loop,duplicates
django,dictionary,loops
loops,range
optimization,loops,for-loop
loops,for-loop,continue
loops,if-statement,case,while-loop
loops,input
loops,dictionary
list,loops
list,loops,conditional-statements
loops,tkinter,pausing-execution
```
```bash
$ grep -E "$pattern" dataset.csv | tr ',' "\n" | sort | uniq -c | sort -nr | head -n 20
```
```
  15458 loops
   2177 list
   1837 for-loop
   1711 pandas
   1398 python-3.x
   1065 while-loop
    975 dictionary
    812 dataframe
    648 function
    563 arrays
    531 numpy
    515 if-statement
    496 iteration
    417 string
    386 python-2.7
    328 csv
    259 variables
    250 tkinter
    249 nested
    211 performance
```
... then 'function':
```bash
$ tag='function'
$ pattern="^$tag,|,$tag,|,$tag$|^$tag$"
$ grep -E -m 30 "$pattern" dataset.csv 
```
```
variables,function,argument-passing
function,scope,closures,attributes
function,arguments
php,function,break
function,main,iterable
django,function
function,decorator
function
django,function,argument-passing
django,function,loops
function,class,methods,python-2.6
function
function,variable-assignment
function,module,variables,global
function,closures,decorator
function,list
list,function
variables,function
function,vector
function
google-app-engine,function
function
function,attributes
oop,function,instance
file,function
file-io,function
function
function,arguments
function,getattr
variables,function
```
```bash
$ grep -E "$pattern" dataset.csv | tr ',' "\n" | sort | uniq -c | sort -nr | head -n 20
```
```
  15340 function
   1928 python-3.x
   1307 list
    877 pandas
    868 class
    660 variables
    648 loops
    558 dictionary
    536 arguments
    526 return
    492 string
    446 tkinter
    443 python-2.7
    442 for-loop
    439 dataframe
    405 if-statement
    377 numpy
    337 recursion
    299 arrays
    290 parameters
```
... then 'javascript':
```bash
$ tag='javascript'
$ pattern="^$tag,|,$tag,|,$tag$|^$tag$"
$ grep -E -m 30 "$pattern" dataset.csv 
```
```
c#,java,javascript,c++
javascript,django,json
javascript,jquery,google-app-engine,blobstore
javascript,scripting
javascript,v8
java,javascript,google-apps-script,google-sheets
javascript,envjs
javascript,django,facebook
javascript,flash,sockets
javascript,urllib2,beautifulsoup,innerhtml
php,javascript,data-warehouse
javascript,websocket
c#,javascript,sql,database
javascript,http,xml-rpc
javascript,selenium,screen-scraping
javascript,html
javascript,translation
javascript
javascript,html,json,recursion
javascript,pyqt,pyqt4,qwebview
javascript,jquery,translation,pylons
php,javascript,ajax,extjs
javascript,django,facebook
javascript,websocket
javascript,performance,coding-style,nested
javascript,json,websocket
javascript,json,text,png
javascript
javascript,compression,libraries,lzw
javascript,screen-scraping
```
... then 'sqlalchemy':
```bash
$ tag='sqlalchemy'
$ pattern="^$tag,|,$tag,|,$tag$|^$tag$"
$ grep -E -m 30 "$pattern" dataset.csv 
```
```
sqlalchemy
sqlalchemy,python-elixir
orm,sqlalchemy
templates,sqlalchemy,x12
sqlalchemy,pylons
sqlalchemy,crud
database-design,sqlalchemy
postgresql,sqlalchemy
sqlalchemy
sqlalchemy
qt,sqlalchemy,pyqt4
sqlalchemy
sqlite,sqlalchemy
sqlalchemy
mysql,sqlalchemy,large-query
sqlalchemy,circular-dependency
sqlalchemy
oracle10g,sqlalchemy
mysql,integer,sqlalchemy
sqlalchemy,orm
sqlalchemy
sql,database,sqlalchemy
sqlalchemy
sqlalchemy
model,sqlalchemy,pylons
session,timeout,sqlalchemy
sqlalchemy
datetime,sqlalchemy
model,sqlalchemy,pylons
sqlalchemy
```
```bash
$ grep -E "$pattern" dataset.csv | tr ',' "\n" | sort | uniq -c | sort -nr | head -n 20
```
```
  15060 sqlalchemy
   2598 flask
   2338 flask-sqlalchemy
   1940 postgresql
   1479 mysql
   1220 sql
    728 sqlite
    700 orm
    625 python-3.x
    606 pandas
    540 database
    377 sql-server
    307 pyramid
    275 alembic
    235 python-2.7
    181 pyodbc
    161 psycopg2
    149 oracle
    147 json
    135 many-to-many
```
... then 'pip':
```bash
$ tag='pip'
$ pattern="^$tag,|,$tag,|,$tag$|^$tag$"
$ grep -E -m 30 "$pattern" dataset.csv 
```
```
pip
pip,packages,setuptools,distutils
pip,setuptools,easy-install,pypi
linux,easy-install,pip,tokyo-cabinet
django,setup-project,virtualenv,pip
windows,mingw,pip,distutils
django,virtualenv,pip
virtualenv,pip,virtualenvwrapper
matplotlib,pip,pypi
dependencies,pip,pypi
django,pip
virtualenv,pip,virtualenvwrapper
setuptools,pip
django,installation,package,pip
distutils,pip
continuous-integration,hudson,virtualenv,pip
pip
ubuntu,virtualenv,pip,mysql-python
development-environment,virtualenv,pip
setuptools,distutils,pip
setuptools,pip
numpy,scipy,virtualenv,pip
pip,packages
macos,ipython,pip
windows,virtualenv,pip
pip,virtualenv,requirements.txt
django,pip
google-app-engine,virtualenv,pip
windows,distutils,pip
windows,installation,pip,easy-install
```
```bash
$ grep -E "$pattern" dataset.csv | tr ',' "\n" | sort | uniq -c | sort -nr | head -n 20
```
```
  15016 pip
   2056 python-3.x
    995 virtualenv
    850 python-2.7
    843 installation
    773 macos
    715 django
    576 setuptools
    567 anaconda
    553 windows
    485 conda
    418 ubuntu
    406 pypi
    372 tensorflow
    371 linux
    370 package
    315 numpy
    271 docker
    270 setup.py
    267 pycharm
```
... then 'pygame':
```bash
$ tag='pygame'
$ pattern="^$tag,|,$tag,|,$tag$|^$tag$"
$ grep -E -m 30 "$pattern" dataset.csv 
```
```
gis,pygame
memory-management,numpy,pygame
pygame
conditional,pygame
pygame,flip
ubuntu,pygame,python-idle
coordinates,pygame,vpython,pyode
pygame,coordinates,geometry-surface
pygame,pgu
pygame,python-import
user-interface,widget,pygame
pygame
animation,pygame
pygame,py2app
graphics,2d,pygame
macos,pygame,cairo
pygame
pygame,sprite,transparent,geometry-surface
installation,pygame
transparency,pygame
list,pygame
pygame,user-profile
pygame,3d-engine,panda3d
events,keyboard,pygame
pygame
windows,pygame
drawing,python-3.x,tkinter,pygame
class,inheritance,pygame
graphics,pygame
pygame,midi
```
```bash
$ grep -E "$pattern" dataset.csv | tr ',' "\n" | sort | uniq -c | sort -nr | head -n 20
```
```
  14795 pygame
   2025 python-3.x
    567 sprite
    531 python-2.7
    396 pygame-surface
    318 image
    297 collision-detection
    269 collision
    259 class
    215 audio
    207 macos
    177 tkinter
    163 pycharm
    162 animation
    144 opengl
    137 raspberry-pi
    126 list
    124 function
    124 blit
    118 pyopengl
```
... then 'multithreading':
```bash
$ tag='multithreading'
$ pattern="^$tag,|,$tag,|,$tag$|^$tag$"
$ grep -E -m 30 "$pattern" dataset.csv 
```
```
multithreading,multicore
java,ruby,multithreading
multithreading,background
multithreading,twisted
events,multithreading,signals,daemon
multithreading
multithreading,thread-safety,urllib2
multithreading,contextmanager
multithreading
multithreading,parallel-processing
multithreading
django,multithreading,subprocess
multithreading,python-idle
c,multithreading,embed
multithreading,cherrypy
multithreading
multithreading,tkinter
multithreading
multithreading,queue,multiprocessing
django,soap,multithreading,asynchronous
sockets,multithreading
linux,multithreading,gtk,pygtk
multithreading,concurrency,datastore
multithreading,pyqt4,qthread
multithreading,gtk,pygtk,clipboard
multithreading
sockets,multithreading,twisted
multithreading
multithreading,arrays
multithreading
```
```bash
$ grep -E "$pattern" dataset.csv | tr ',' "\n" | sort | uniq -c | sort -nr | head -n 20
```
```
  13783 multithreading
   1502 multiprocessing
   1386 python-3.x
   1107 python-multithreading
    609 tkinter
    594 python-2.7
    573 sockets
    443 queue
    378 pyqt
    317 parallel-processing
    309 flask
    274 django
    268 python-multiprocessing
    261 concurrency
    242 asynchronous
    231 pyqt5
    226 python-asyncio
    222 subprocess
    201 thread-safety
    196 threadpool
```
... and finally 'windows':
```bash
$ tag='windows'
$ pattern="^$tag,|,$tag,|,$tag$|^$tag$"
$ grep -E -m 30 "$pattern" dataset.csv 
```
```
windows,unicode,file-io
windows,py2exe
windows,windows-installer
windows,dll,dllimport,ctypes
windows,parsing,lxml
windows,scrapy
windows,environment-variables
windows,ssh,tunneling,ssh-tunnel
windows,symlink
windows
windows,windows-7,soft-keyboard
windows,window,curses
windows,linux,macos,audio
c++,windows,unit-testing,dll
windows
windows,proxy,urllib
windows,web-crawler,scrapy
windows,django,unicode
windows,winapi,pywin32
windows,csv,newline
windows,proxy
windows
windows,process,build-automation,fork
windows,archive,python-2.6
windows,unicode,python-2.x,python-unicode
windows,unicode,console,pymssql
windows,system
windows,django,python-imaging-library,virtualenv
windows,mmap
windows,linux,twisted
```
```bash
$ grep -E "$pattern" dataset.csv | tr ',' "\n" | sort | uniq -c | sort -nr | head -n 20
```
```
  13081 windows
   1441 python-3.x
    739 python-2.7
    553 pip
    487 linux
    468 cmd
    442 subprocess
    359 anaconda
    302 django
    297 tkinter
    284 batch-file
    281 pyinstaller
    266 installation
    218 winapi
    206 tensorflow
    196 c++
    194 pywin32
    183 powershell
    182 path
    181 virtualenv
```

---

That's all for now!
