from urllib2 import Request, urlopen, URLError
import xml.etree.ElementTree as ET
import datetime
import psycopg2
import os
import urlparse
'''
thisItem = '2399'
thisSystem = '30002187'
request = Request('http://api.eve-central.com/api/marketstat?typeid=' + thisItem + '&usesystem=' + str(thisSystem))
try:
    response = urlopen(request)
    data = response.read()
    root = ET.fromstring(data)
    print(data)
    print(root[0][0][1][6].text)
    #    print(child.tag, child.attrib)
    #CommodityDict[thisItem]['SellPrice'] = root[0][0][1][6].text

except URLError, e:
    print 'error code:', e
'''
thisSystem = '30002187'
thisItem = '2399'

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

print thisItem
print fetchSellPrice(thisSystem,thisItem)
print datetime.datetime.now()

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
cur.execute('SELECT id FROM name')
rows = cur.fetchall()

for row in rows:
    print row[0]


if con:
    con.close()