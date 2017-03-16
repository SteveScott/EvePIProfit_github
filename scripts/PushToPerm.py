from urllib import parse, request
import xml.etree.ElementTree as ET
import datetime
import psycopg2
import os
import eveLists
import connection

os.environ['DATABASE_URL']='postgres://lojyjajvpwaaci:4ya_0u6olTZ2taL68me6Goa1HD@ec2-54-243-199-161.compute-1.amazonaws.com:5432/deaek2i6u7a13g'
parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ["DATABASE_URL"])

con = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

def main():
    con = connection.establish_connection()
    cur = con.cursor()
    cur.execute("INSERT INTO PERM_JITA SELECT * FROM TEMP_JITA;")
    cur.execute("INSERT INTO PERM_AMARR SELECT * FROM TEMP_AMARR;")
    cur.execute("INSERT INTO PERM_RENS SELECT * FROM TEMP_RENS;")
    cur.execute("INSERT INTO PERM_DODIXIE SELECT * FROM TEMP_DODIXIE;")
    cur.close()
    con.commit()
    con.close()
    return 0

