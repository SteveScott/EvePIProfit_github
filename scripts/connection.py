import psycopg2
from urllib import request, parse
import os

os.environ['DATABASE_URL']='postgres://lojyjajvpwaaci:4ya_0u6olTZ2taL68me6Goa1HD@ec2-54-243-199-161.compute-1.amazonaws.com:5432/deaek2i6u7a13g'
parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ["DATABASE_URL"])

def establish_connection():
    try:
        con = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        return con
    except:
        print("failed to connect to database")
