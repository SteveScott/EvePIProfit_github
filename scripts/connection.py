import psycopg2
from urllib import request, parse
import os


#parse.uses_netloc.append("postgres")
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




