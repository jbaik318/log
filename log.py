#!/usr/bin/env python

import psycopg2
import sys

# tables artcles and log were join through fields slug and path.
# field slug contained the articles directory and thus required
# concatination to match field path
query1 = """select articles.title, count(*) as num
                from articles
                join log
                on concat('/article/',articles.slug,'') = log.path
                where status='200 OK'
                group by articles.title
                order by num
                desc limit 3"""

# This query utilizes the results from the previous query question as a
# subquery.
# This query matches the author's id to the name of each author
query2 = """select authors.name, sq.num
                from (select articles.author as authors, count(*) as num
                        from articles
                        join log
                        on concat('/article/',articles.slug,'') = log.path
                        where status='200 OK'
                        group by articles.author
                        order by num
                        desc) as sq
                join authors
                on sq.authors = authors.id
                group by authors.name, sq.num
                order by sq.num
                desc;"""

# this query utilizes two subqueries that are very similar to one another.
# The first subquery selects all GET requests per day
# The second subquery select all non-sucessful GET request per day
# fm was used before Month to remove 9 blankspace
# percentage of error was found be dividing accountants of error
# to total GET requests. Then multiplied by 100
# during the caluclation, the numbers can to be set to float and numeric
# to recieve proper decimal points.
query3 = """select to_char(error.date, 'FMMonth FMDD, YYYY') as date
                   ,round(((error.errors/total.total::float)*100)::numeric,1)
               as percent
                from (select date(time)
                as date, count(*) as total
                        from log
                        where method = 'GET'
                        group by date(time)
                        order by total
                        desc) as total
               join (select date(time)
               as date, count(*) as errors
                        from log
                        where status = '404 NOT FOUND'
                        group by date(time)
                        order by errors
                        desc) as error
                on total.date = error.date
                where
                round(((error.errors/total.total::float)*100)::numeric,1) >1
                group by error.date, percent
                order by percent
                desc;"""


def connect(database_name):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect('dbname={}'.format(str(database_name)))
        return db
    except psycopg2.Error as e:
        print ("Unable to connect to database")
        # exit the program
        sys.exit(1)


def get_query_results(query):
    # establishes connection to the news data base
    db = connect("news")
    # sets c to interact with psql queries
    c = db.cursor()
    # executes the psql query
    c.execute(query)
    # sets post as the result of psql query
    post = c.fetchall()
    # closes the database
    db.close()
    return post


def top_articles():
    print("Top three most viewed articles")
    for x in get_query_results(query1):
        print('"{}" - {} views'.format(x[0], str(x[1])))


def top_authors():
    print("\nAuthor views")
    for x in get_query_results(query2):
        print('{} - {} views'.format(x[0], str(x[1])))


def sig_error():
    print("\nDay where errors occured more than 1% of total")
    for x in get_query_results(query3):
        print('{} - {}%'.format(x[0], str(x[1])))

if __name__ == '__main__':
    top_articles()
    top_authors()
    sig_error()
else:
    print("This file is imported")
