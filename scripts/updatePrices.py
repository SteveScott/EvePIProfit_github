from urllib2 import Request, urlopen, URLError
import xml.etree.ElementTree as ET
import datetime
import psycopg2
import os
import urlparse
import scripts.eveLists
from scripts import connection


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
def main():
    ###Establish connection
    con = connection.establish_connection()

    ###clear the database
    cur = con.cursor()
    print('truncating PRICE_TEMP')
    cur.execute('TRUNCATE TABLE PRICE_TEMP')
    cur.close()
    con.commit()



    #get each price and put it in the database
    '''
    for i in eveLists.systemList:
        for j in eveLists.itemList:
            tempPrice = fetchSellPrice(i,j)
            print datetime.date.today(), datetime.datetime.utcnow().time(), i, " ", j, " ", tempPrice
            cur = con.cursor()
            cur.execute('INSERT INTO PRICE_TEMP VALUES (%s, %s, %s, NULL, %s, %s, NULL)', (str(j), str(i), float(tempPrice), datetime.date.today(), datetime.datetime.utcnow()))
    '''

    i = 30000142
    cur = con.cursor()
    print('truncating TEMP_JITA')
    cur.execute('TRUNCATE TABLE TEMP_JITA')
    cur.close()

    for j in scripts.eveLists.itemList:
        tempPrice = fetchSellPrice(i,j)
        print datetime.date.today(), datetime.datetime.utcnow().time(), i, " ", j, " ", tempPrice
        cur = con.cursor()
        cur.execute('INSERT INTO TEMP_JITA VALUES (%s, %s, %s, NULL, %s, %s, NULL)', (str(j), str(i), float(tempPrice), datetime.date.today(), datetime.datetime.utcnow()))
        cur.close()
        con.commit()

    i = 30002187
    cur = con.cursor()
    cur.execute('TRUNCATE TABLE TEMP_AMARR')
    cur.close()
    for j in scripts.eveLists.itemList:
        tempPrice = fetchSellPrice(i,j)
        print datetime.date.today(), datetime.datetime.utcnow().time(), i, " ", j, " ", tempPrice
        cur = con.cursor()
        cur.execute('INSERT INTO TEMP_AMARR VALUES (%s, %s, %s, NULL, %s, %s, NULL)', (str(j), str(i), float(tempPrice), datetime.date.today(), datetime.datetime.utcnow()))
        cur.close()
        con.commit()

    i = 30002510
    cur = con.cursor()
    cur.execute('TRUNCATE TABLE TEMP_RENS')
    cur.close()
    for j in scripts.eveLists.itemList:
        tempPrice = fetchSellPrice(i,j)
        print datetime.date.today(), datetime.datetime.utcnow().time(), i, " ", j, " ", tempPrice
        cur = con.cursor()
        cur.execute('INSERT INTO TEMP_RENS VALUES (%s, %s, %s, NULL, %s, %s, NULL)', (str(j), str(i), float(tempPrice), datetime.date.today(), datetime.datetime.utcnow()))
        cur.close()
        con.commit()

    i = 30002659
    cur = con.cursor()
    cur.execute('TRUNCATE TABLE TEMP_DODIXIE')
    cur.close()
    for j in scripts.eveLists.itemList:
        tempPrice = fetchSellPrice(i,j)
        print datetime.date.today(), datetime.datetime.utcnow().time(), i, " ", j, " ", tempPrice
        cur = con.cursor()
        cur.execute('INSERT INTO TEMP_DODIXIE VALUES (%s, %s, %s, NULL, %s, %s, NULL)', (str(j), str(i), float(tempPrice), datetime.date.today(), datetime.datetime.utcnow()))
        cur.close()
        con.commit



    if con:
        con.commit()
        con.close()
