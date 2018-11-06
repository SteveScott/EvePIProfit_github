from urllib import request, error, parse
import xml.etree.ElementTree as ET
import datetime
import psycopg2
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import asyncio

import eveLists
import connection

con = connection.establish_connection()
cur = con.cursor()

async def LookupPrice(item, cur):
    cur.execute('SELECT price FROM PRICE_TEMP WHERE itemid = %s;', [item])
    answer = cur.fetchall()

    if len(answer) > 0:
        #print('The lookup price answer is %s', answer[0][0])
        return answer[0][0]
    else:
        #print('the answer has length 0.')
        return 0

async def lookup_buy_price(item, cur):
    cur.execute('SELECT buy_price FROM PRICE_TEMP WHERE itemid = %s;', [item])
    answer = cur.fetchall()

    if len(answer) > 0:
        # print('The lookup price answer is %s', answer[0][0])
        return answer[0][0]
    else:
        # print('the answer has length 0.')
        return 0

async def CalculateProfit(system1, item1, cur, con):

    cur.execute('SELECT * FROM recipe WHERE ID = %s;', [item1])
    tempList = cur.fetchall()

    i0 = 0
    i1 = 0
    i2 = 0
    i3 = 0
    q0 = 1
    p1 = 0
    q1 = 0
    p2 = 0
    q2 = 0
    p3 = 0
    q3 = 0

    if (len(tempList) > 0):
        i0 = tempList[0][0]
        q0 = tempList[0][1]
        i1 = tempList[0][2]
        q1 = tempList[0][3]
        i2 = tempList[0][4]
        q2 = tempList[0][5]
        i3 = tempList[0][6]
        q3 = tempList[0][7]
        p0 = await LookupPrice(i0, cur)
        p1 = await LookupPrice(i1, cur)
        p2 = await LookupPrice(i2, cur)
        p3 = await LookupPrice(i3, cur)
        p0b = await lookup_buy_price(i0, cur)
        p1b = await lookup_buy_price(i1, cur)
        p2b = await lookup_buy_price(i2, cur)
        p3b = await LookupPrice(i3, cur)

    #produced = # [tempList[1]


        if ((p0 == 0 or p0b == 0) or (q1 > 0 and (p1 == 0 or p1b == 0)) or (q2 > 0 and (p2 == 0 or p2b == 0)) or (q3 > 0 and (p3 == 0 or p3b == 0))):
            #print(str(i0) + " no price found for one of the commodities")

            marginalProfit = 0
            percentProfit = 0
            marginalCost = 0
            marginal_buy_cost = 0

        else:

            marginalCost = (p1 * q1 + p2 * q2 + p3 * q3) / q0
            marginal_buy_cost = ((p1b * q1 + p2b * q2 + p3b * q3)/ q0)
            salePrice = await LookupPrice(item1, cur)
            marginalProfit = salePrice - marginalCost
            percentProfit = ((marginalProfit) * 100) / salePrice

        #print("updating", i0, p0, p1, q1, p2, q2, p3, q3)
        cur.execute('UPDATE PRICE_TEMP SET PROFIT = %s, PROFITMARGIN = %s, COST = %s, BUY_COST = %s WHERE ITEMID = %s;', (marginalProfit, percentProfit, marginalCost, marginal_buy_cost, item1))
        con.commit()


    else:
        try:
            marginalProfit = 0
            percentProfit = 0
            marginalCost = 0
            marginal_buy_cost = 0
            #print('len(tempList) = 0')
            cur.execute("UPDATE PRICE_TEMP SET PROFIT = %s, PROFITMARGIN = %s, COST = %s, BUY_COST = %s WHERE ITEMID = %s;", (marginalProfit, percentProfit, marginalCost, marginal_buy_cost, item1))

        except:
            print('exception ')

def ClearTemp(cur, con):

    #print("truncating table price_temp")
    try:
        cur.execute('TRUNCATE TABLE price_temp')
    except Exception as e:
        print(e)
        print("trying again")
        try:
            con = connection.establish_connection()
            cur = con.cursor()
            cur.execute('TRUNCATE TABLE price_temp;')

        except Exception as e:
            print(e.message)
            print("failed to connect a second time.")
    con.commit()
    #print("price_temp truncated")

async def mainLoop():

    for i in eveLists.systemList:
        ClearTemp(cur, con)
        databaseName = eveLists.databaseDict[i]
        ###added after broke. need to repoppulate price_temp with system data

        cur.execute("INSERT INTO PRICE_TEMP SELECT * FROM {0};".format(databaseName))
        con.commit()
        try:
            for j in eveLists.itemList:
                await CalculateProfit(i, j, cur, con)
        finally:

            cur.execute('UPDATE PRICE_TEMP SET PROFITMARGIN = 0, PROFIT = 0 WHERE PROFIT IS NULL;')
            cur.execute('UPDATE PRICE_TEMP SET COST = 0 WHERE COST IS NULL;')
            cur.execute('UPDATE PRICE_TEMP SET BUY_COST = 0 WHERE BUY_COST IS NULL;')

            cur.execute('DROP TABLE {0};'.format(databaseName))
            cur.execute(
                'CREATE TABLE {0} AS SELECT itemid,mysystem,price,profitmargin,mydate,mytime,profit,cost,buy_price, buy_cost FROM PRICE_TEMP;'.format(
                    databaseName))
            print("creating table {0}".format(eveLists.databaseDict[i]))

###Main###
def main():

    print("Calculating Profit")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(mainLoop())
    loop.close()
    cur.close()
    con.commit()
    con.close()
    print("calculateMargins complete")
    return 0

