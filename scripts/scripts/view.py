from urllib2 import Request, urlopen, URLError
import xml.etree.ElementTree as ET
import datetime
import psycopg2
import os
import urlparse
import eveLists


urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

con = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

cur = con.cursor()
cur.execute('SELECT * FROM PRICE_TEMP')
printme = cur.fetchall()
i = 0
while (i <  len(printme)):
    print printme[i]
    i += 1

cur.close()
con.close()