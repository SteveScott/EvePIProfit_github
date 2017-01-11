from urllib2 import Request, urlopen, URLError
import xml.etree.ElementTree as ET
import datetime
import psycopg2
import os
import urlparse
import scripts.eveLists

os.environ['DATABASE_URL']='postgres://lojyjajvpwaaci:4ya_0u6olTZ2taL68me6Goa1HD@ec2-54-243-199-161.compute-1.amazonaws.com:5432/deaek2i6u7a13g'
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

con = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

def Main():
    cur = con.cursor()
    cur.execute("INSERT INTO JITA_PERM SELECT * FROM JITA_TEMP;")
    cur.execute("INSERT INTO AMARR_PERM SELECT * FROM AMARR_TEMP;")
    cur.execute("INSERT INTO RENS_PERM SELECT * FROM RENS_TEMP;")
    cur.execute("INSERT INTO DODIXIE_PERM SELECT * FROM DODIXIE_TEMP;")
    cur.close()
    con.commit()
    con.close()
    return 0

