import os
import psycopg2
from urllib import request, parse
from flask_sqlalchemy import SQLAlchemy


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


