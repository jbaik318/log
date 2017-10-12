#Log Project

This project uses python and postgreSQL to interact with a news article database.

Log.py answers three questions
* What are the top three most viewed articles in the database
* How many views do each author have 
* On what day were there more than 1% error when viewing an article

#Setup Guide

log.py will not run unless the postgreSQL in installed in the device

- open terminal
- install postgresql
- pip installation
```sh
	pip install psycopg2
```
- download the database (newsdata.sql) from the following link (https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and download into the same directory as log.py
- load the database and set as "_news_"
```sh
	psql -d news -f newsdata.sql
```
- run the file 
``` sh
	python3 log.py
```
	or
```sh
	python log.py
```

