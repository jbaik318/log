#!/usr/bin/env python

import psycopg2


query1 = """select articles.title, count(*) as num
                from articles
                join log
                on concat('/article/',articles.slug,'') = log.path
                where status='200 OK'
                group by articles.title
                order by num
                desc limit 3"""

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


def get_query_results(query):
    db = psycopg2.connect(dbname="news")
    c = db.cursor()
    c.execute(query)
    post = c.fetchall()
    db.close()
    return post

print("Top three most viewed articles")

for x in get_query_results(query1):
    print('"{}" - {} views'.format(x[0], str(x[1])))

print("\nAuthor views")

for x in get_query_results(query2):
    print('{} - {} views'.format(x[0], str(x[1])))

print("\nDay where errors occured more than 1% of total")

ans3 = []
for x in get_query_results(query3):
    print('{} - {}%'.format(x[0], str(x[1])))
