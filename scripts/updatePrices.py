from urllib import request, error, request
import xml.etree.ElementTree as ET
import datetime
import psycopg2
import sys
print("sys.path:")
print(sys.path)
from psycopg2 import sql
import os
import os.path
import urllib.parse
#import eveLists
#import connection
import atexit
from psycopg2.extensions import AsIs, quote_ident

#sys.path.append("~/Dropbox/1programming2/EVE/EvePIProfit_github")





def fetchSellPrice(thisSystem, thisItem):

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


def main(con):
    ###Establish connection
    print("establishing connection")
    #con = connection.establish_connection()
    con.autocommit = True
    cur = con.cursor()



    for i in eveLists.systemList:
        database_name = eveLists.databaseDict[i]
        #'''
        #clear the database

        #print (sql.SQL("TRUNCATE TABLE {};").format(sql.Identifier(database_name)))
        try:
            #cur.execute('TRUNCATE TABLE temp_jita;')
            cur.execute(sql.SQL('TRUNCATE TABLE {};').format(sql.Identifier(database_name)))
            print(("Table {} truncated").format(database_name))
        except:
            print(("failed to truncate table {}.").format(database_name))
        #cur.execute("TRUNCATE TABLE temp_jita;")
        #print("table truncated")
        #'''
        #insert into the database
        print("inserting into ", eveLists.systemDictReverse[i])
        for j in eveLists.itemList:
            tempPrice = fetchSellPrice(i, j)

            now = str(datetime.datetime.utcnow())
            try:
                cur.execute(sql.SQL("INSERT INTO {} VALUES (%s, %s, %s, NULL, %s, %s, NULL, NULL);").format(sql.Identifier(database_name)),[
                                                                                        str(j),
                                                                                        str(i),
                                                                                        float(tempPrice),
                                                                                        datetime.date.today(),
                                                                                        now])
                #print( j, "Executed")
            except:
                print("Cannot insert")

    con.commit()
    print("updatePrices complete")
    cur.close()
    #con.close()


    '''
    # get each price and put it in the database
    i = 30000142
    print("inserting into ", eveLists.systemDictReverse[i])
    for j in eveLists.itemList:
        tempPrice = fetchSellPrice(i, j)
        # database_name = eveLists.DatabaseDict[i]
        now = datetime.datetime.utcnow()
        now = str(now)

        cur.execute("INSERT INTO temp_jita VALUES (%s, %s, %s, NULL, %s, %s, NULL);", [  # database_name,
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

    i = 30002659
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
    '''






