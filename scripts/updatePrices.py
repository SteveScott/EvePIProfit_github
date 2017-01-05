from urllib2 import Request, urlopen, URLError
import xml.etree.ElementTree as ET
import datetime
import psycopg2
import os
import urlparse
import eveLists

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

def fetchSellPrice(thisSystem, thisItem):
    request = Request('http://api.eve-central.com/api/marketstat?' +
                      'typeid=' + str(thisItem) +
                      '&usesystem=' + str(thisSystem))
    try:
        response = urlopen(request)
        data = response.read()
        root = ET.fromstring(data)
        return root[0][0][1][6].text
    except URLError, e:
        print 'error code:', e

#print thisItem
#print fetchSellPrice(thisSystem,thisItem)
#print datetime.datetime.now()

###clear the database
cur=con.cursor()
cur.execute('TRUNCATE TABLE PRICE_TEMP')
cur.close()
con.commit()



#get each price and put it in the database

for i in eveLists.systemList:
    for j in eveLists.itemList:
        tempPrice = fetchSellPrice(i,j)
        print datetime.date.today(), datetime.datetime.utcnow().time(), i, " ", j, " ", tempPrice
        cur = con.cursor()
        cur.execute('INSERT INTO PRICE_TEMP VALUES (%s, %s, %s, NULL, %s, %s, NULL)', (str(j), str(i), float(tempPrice), datetime.date.today(), datetime.datetime.utcnow()))


'''
cur = con.cursor()
cur.execute('SELECT id FROM name')
rows = cur.fetchall()
itemList = []
for row in rows:
    itemList.append(row[0])

print itemList
'''

if con:
    con.commit()
    con.close()