import os
import psycopg2
from urllib import request, parse

'''
parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ["DATABASE_URL"])

print("host:" + url.hostname)

def establish_connection():
    try:
        con = psycopg2.connect(
            dbname=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port,
        )

        return con
    except:
        print("failed to connect to database")


'''

def establish_connection():
    #print(os.environ['DATABASE_NAME'])
    #print(os.environ['DATABASE_USER'])
    #print(os.environ['DATABASE_PASSWORD'])
    #print(os.environ['DATABASE_HOST'])
    #print(os.environ['PORT'])

    try:

        con = psycopg2.connect(
            dbname=os.environ.get("DATABASE_NAME"),
            user=os.environ.get("DATABASE_USER"),
            password=os.environ.get("DATABASE_PASSWORD"),
            host=os.environ.get("DATABASE_HOST"),
            port=os.environ.get("DATABASE_PORT")
        )

        return con

    except:
        print("failed to connect to database.")


