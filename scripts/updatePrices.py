import atexit
import datetime
import os
import os.path
import psycopg2
import sys
import urllib.parse
import xml.etree.ElementTree as ET
from psycopg2 import sql
from psycopg2.extensions import AsIs, quote_ident
from urllib import request, error, request

import scripts.connection
import scripts.eveLists
import fetchPrices


def fetchSellPrice(thisSystem, thisItem):
    #print("")
    #print("thisSystem = " + str(thisSystem) + " thisItem = " + str(thisItem))
    systemName = scripts.eveLists.systemDictReverse[thisSystem]
    station = scripts.eveLists.systemToStation[systemName]
    #print(station)
    region = scripts.eveLists.systemToRegion[systemName]
    #print(region)
    region_id = scripts.eveLists.regionId[region]
    #print(region_id)
    answer = fetchPrices.find_price("sell", thisItem, region_id, station)
    #print(answer)
    return answer

def fetchBuyPrice(thisSystem, thisItem):
    systemName = scripts.eveLists.systemDictReverse[thisSystem]
    station = scripts.eveLists.systemToStation[systemName]
    region = scripts.eveLists.systemToRegion[systemName]
    region_id = scripts.eveLists.regionId[region]
    answer = fetchPrices.find_price("buy", thisItem, region_id, station)
    #print(("Buy Price {0}").format(answer) or "Buy Price null")
    return answer


def main():
    ###Establish connection
    print("establishing connection")
    con = scripts.connection.establish_connection()
    con.autocommit = False
    cur = con.cursor()



    for i in scripts.eveLists.systemList:
        database_name = scripts.eveLists.databaseDict[i]
        #'''
        #clear the database
        print(database_name)
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
        print("inserting into ", scripts.eveLists.systemDictReverse[i])
        for j in scripts.eveLists.itemList:
            tempSellPrice = fetchSellPrice(i, j)
            try:
                tempSellPrice = float(tempSellPrice)
            except:
                tempSellPrice = 0

            tempBuyPrice = fetchBuyPrice(i, j)
            try:
                tempBuyPrice = float(tempBuyPrice)
            except:
                tempBuyPrice = 0

            now = str(datetime.datetime.utcnow())
            try:
                cur.execute(sql.SQL("INSERT INTO {} VALUES (%s, %s, %s, NULL, %s, %s, NULL, NULL, %s, NULL);").format(sql.Identifier(database_name)), [
                                                                                        str(j),
                                                                                        str(i),
                                                                                        float(tempSellPrice) ,
                                                                                        datetime.date.today(),
                                                                                        now,
                                                                                        float(tempBuyPrice)])
               # print(j, "Executed")
            except:
                print("Error cannot insert")

    con.commit()
    print("updatePrices complete")
    cur.close()
    con.close()


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






