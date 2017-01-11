from urllib2 import Request, urlopen, URLError
import xml.etree.ElementTree as ET
import datetime
import psycopg2
import os
import urlparse
import scripts.eveLists
from scripts import connection


def LookupPrice(item, cur):
    print(item)
    cur.execute('SELECT PRICE FROM PRICE_TEMP WHERE ITEMID = %s', [item])
    answer = cur.fetchall()
    if len(answer) > 0:
        print('The lookup price answer is %s', answer[0][0])
        return answer[0][0]
    else:
        #print('the answer has length 0.')
        return 0


def CalculateProfit(system1, item1) :
    con = connection.establish_connection()
    cur = con.cursor()
    cur.execute('SELECT * FROM recipe WHERE ID = %s', [item1])
    tempList = cur.fetchall()
    id = 0
    q0 = 1
    p1 = 0
    q1 = 0
    p2 = 0
    q2 = 0
    p3 = 0
    q3 = 0

    if (len(tempList) > 0):
        id = tempList[0][0]
        q0 = tempList[0][1]
        p1 = tempList[0][2]
        q1 = tempList[0][3]
        p2 = tempList[0][4]
        q2 = tempList[0][5]
        p3 = tempList[0][6]
        q3 = tempList[0][7]

    #produced = # [tempList[1]


    if len(tempList) > 0:
        try:
            netCost = ((LookupPrice(p1, cur)*q1 + LookupPrice(p2, cur)*q2 + LookupPrice(p3, cur)*q3) / q0)
            salePrice = LookupPrice(item1, cur)
            netProfit = salePrice - netCost
            percentProfit = ((salePrice - netCost) * 100) / netCost
            print item1, LookupPrice(item1, cur),((LookupPrice(p1, cur)*q1 + LookupPrice(p2, cur)*q2 + LookupPrice(p3, cur)*q3) / q0)
        except ZeroDivisionError:
            netProfit = 0
            percentProfit = 0
            print('zero division error, default to 0')
        print item1
        cur.execute('UPDATE PRICE_TEMP SET PROFIT = %s, PROFITMARGIN = %s WHERE ITEMID = %s', (netProfit, percentProfit, item1))
        con.commit()
        cur.close()
        con.close()

    else:
        try:
            netProfit = 0
            percentProfit = 0
            cur = con.cursor()
            print('0')
            cur.execute("UPDATE PRICE_TEMP SET PROFIT = %s, PROFITMARGIN = %s WHERE ITEMID = %s", (netProfit, percentProfit, item1))
        except:
            print('exception')

def ClearTemp():
    con = connection.establish_connection()
    cur = con.cursor()
    cur.execute('TRUNCATE TABLE price_temp')
    cur.close()
    con.commit()
    con.close()


###Main###
def main():


    for i in scripts.eveLists.systemList:
        ClearTemp()
        databaseName = scripts.eveLists.DatabaseDict[i]
    ###added after broke. need to repoppulate price_temp with system data
        con = connection.establish_connection()
        cur = con.cursor()
        cur.execute("INSERT INTO PRICE_TEMP SELECT * FROM {0};".format(databaseName))
        cur.close()

    ####
        for j in scripts.eveLists.itemList:
            CalculateProfit(i, j)

        cur = con.cursor()
        cur.execute('DROP TABLE {0}'.format(databaseName))
        cur.execute('CREATE TABLE {0} AS SELECT itemid, mysystem, price, profitmargin,mydate,mytime,profit FROM price_temp'.format(databaseName))
        cur.close()
        con.commit()
        con.close()


