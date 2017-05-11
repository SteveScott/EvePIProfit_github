from urllib import request, error, request
import xml.etree.ElementTree as ET
import datetime
import psycopg2
import os
import urllib.parse
import eveLists
import connection
import sys
import atexit

sys.path.append("~/Dropbox/1programming2/EVE/EvePIProfit_github")


def fetchSellPrice(thisSystem, thisItem):
    # print("fetching sell price")

    request = urllib.request.urlopen('http://api.eve-central.com/api/marketstat?' +
                                     'typeid=' + str(thisItem) +
                                     '&usesystem=' + str(thisSystem))

    try:
        response = request  # urllib.request.urlopen(request)
        data = response.read()
        root = ET.fromstring(data)
        return root[0][0][1][6].text
    except:
        print("error fetching sell price")

# print thisItem
# print fetchSellPrice(thisSystem,thisItem)
# print datetime.datetime.now()
def main():
    ###Establish connection
    try:
        con = connection.establish_connection()
    except():
        print("couldn't establish connection")

    ###clear the database
    cur = con.cursor()

    # get each price and put it in the database

    #for i in eveLists.systemList:
    i = 30000142
    print("inserting into ", eveLists.systemDictReverse[i])
    for j in eveLists.itemList:
        tempPrice = fetchSellPrice(i, j)
        #database_name = eveLists.DatabaseDict[i]
        now = datetime.datetime.utcnow()
        now = str(now)

        cur.execute("INSERT INTO temp_jita VALUES (%s, %s, %s, NULL, %s, %s, NULL);", [#database_name,
                                                                                str(i),
                                                                                str(j),
                                                                                float(tempPrice),
                                                                                datetime.date.today(),
                                                                                now
                                                                                ])

    i = 30002187
    print("inserting into ", eveLists.systemDictReverse[i])
    for j in eveLists.itemList:
        tempPrice = fetchSellPrice(i, j)
        # database_name = eveLists.DatabaseDict[i]
        now = datetime.datetime.utcnow()
        now = str(now)

        cur.execute("INSERT INTO temp_amarr VALUES (%s, %s, %s, NULL, %s, %s, NULL);", [  # database_name,
                                                                                            str(i),
                                                                                            str(j),
                                                                                            float(tempPrice),
                                                                                            datetime.date.today(),
                                                                                            now
                                                                                        ])

    i = 30002510
    print("inserting into ", eveLists.systemDictReverse[i])
    for j in eveLists.itemList:
        tempPrice = fetchSellPrice(i, j)
        # database_name = eveLists.DatabaseDict[i]
        now = datetime.datetime.utcnow()
        now = str(now)

        cur.execute("INSERT INTO temp_rens VALUES (%s, %s, %s, NULL, %s, %s, NULL);", [  # database_name,
                                                                                            str(i),
                                                                                            str(j),
                                                                                            float(tempPrice),
                                                                                            datetime.date.today(),
                                                                                            now
                                                                                        ])

    ii = 30002659
    print("inserting into ", eveLists.systemDictReverse[i])
    for j in eveLists.itemList:
        tempPrice = fetchSellPrice(i, j)
        # database_name = eveLists.DatabaseDict[i]
        now = datetime.datetime.utcnow()
        now = str(now)

        cur.execute("INSERT INTO temp_dodixie VALUES (%s, %s, %s, NULL, %s, %s, NULL);", [  # database_name,
                                                                                            str(i),
                                                                                            str(j),
                                                                                            float(tempPrice),
                                                                                            datetime.date.today(),
                                                                                            now
                                                                                        ])

    con.commit()
    print("updatePrices complete")
    cur.close()
    con.close()







