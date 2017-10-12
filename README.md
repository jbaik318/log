This project connects to a database of articles and repective information. 

Log.py answers three questions
Q1 - What are the top three most viewed articles in the database
Q2 - How many views do each author have 
Q3 - On what day were there more than 1% error when viewing an article

log.py will contain additional commentary that will guide and explain the process of answering these questions. 


Setup Guide

log.py will not run unless the postgreSQL in installed in the device
1. open terminal
2. install postgresql
	pip option: 
		pip install psycopg2
3. download the database (newsdata.sql) from the following link (https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and download into the same directory as log.py
4. to load the data on 
		psql -d news -f newsdata.sql
5. then run the file 
		python3 log.py
			or
		python log.py


