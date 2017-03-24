from urllib import request, error, request
import xml.etree.ElementTree as ET
import datetime
import psycopg2
import os
import urllib.parse
import eveLists
import connection
import sys

sys.path.append("~/Dropbox/1programming2/EVE/EvePIProfit_github")


def fetchSellPrice(thisSystem, thisItem):
    print("fetching sell price")

    request = urllib.request.urlopen('http://api.eve-central.com/api/marketstat?' +
                      'typeid=' + str(thisItem) +
                      '&usesystem=' + str(thisSystem))

    try:
        response = request#urllib.request.urlopen(request)
        data = response.read()
        root = ET.fromstring(data)
        return root[0][0][1][6].text
    except:
        print("error fetching sell price")

#print thisItem
#print fetchSellPrice(thisSystem,thisItem)
#print datetime.datetime.now()
def main():
    ###Establish connection
    try:
        con = connection.establish_connection()
    except():
        print("couldn't establish connection")

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
    try:
        cur.execute('TRUNCATE TABLE TEMP_JITA')
        print("Jita truncated")
    except:
        print("Jita not truncated")
    cur.close()

    for j in eveLists.itemList:
        tempPrice = fetchSellPrice(i,j)
        print(datetime.date.today(), datetime.datetime.utcnow().time(), i, " ", j, " ", tempPrice)
        cur = con.cursor()
        cur.execute('INSERT INTO TEMP_JITA VALUES (%s, %s, %s, NULL, %s, %s, NULL)', (str(j), str(i), float(tempPrice), datetime.date.today(), datetime.datetime.utcnow()))
        cur.close()
        con.commit()

    i = 30002187
    cur = con.cursor()
    cur.execute('TRUNCATE TABLE TEMP_AMARR')
    cur.close()
    for j in eveLists.itemList:
        tempPrice = fetchSellPrice(i,j)
        print(datetime.date.today(), datetime.datetime.utcnow().time(), i, " ", j, " ", tempPrice)
        cur = con.cursor()
        cur.execute('INSERT INTO TEMP_AMARR VALUES (%s, %s, %s, NULL, %s, %s, NULL)', (str(j), str(i), float(tempPrice), datetime.date.today(), datetime.datetime.utcnow()))
        cur.close()
        con.commit()

    i = 30002510
    cur = con.cursor()
    cur.execute('TRUNCATE TABLE TEMP_RENS')
    cur.close()
    for j in eveLists.itemList:
        tempPrice = fetchSellPrice(i,j)
        print(datetime.date.today(), datetime.datetime.utcnow().time(), i, " ", j, " ", tempPrice)
        cur = con.cursor()
        cur.execute('INSERT INTO TEMP_RENS VALUES (%s, %s, %s, NULL, %s, %s, NULL)', (str(j), str(i), float(tempPrice), datetime.date.today(), datetime.datetime.utcnow()))
        cur.close()
        con.commit()

    i = 30002659
    cur = con.cursor()
    cur.execute('TRUNCATE TABLE TEMP_DODIXIE')
    cur.close()
    for j in eveLists.itemList:
        tempPrice = fetchSellPrice(i,j)
        print(datetime.date.today(), datetime.datetime.utcnow().time(), i, " ", j, " ", tempPrice)
        cur = con.cursor()
        cur.execute('INSERT INTO TEMP_DODIXIE VALUES (%s, %s, %s, NULL, %s, %s, NULL)', (str(j), str(i), float(tempPrice), datetime.date.today(), datetime.datetime.utcnow()))
        cur.close()
        con.commit



    if con:
        con.commit()
        con.close()
