from urllib import request, error, parse
import xml.etree.ElementTree as ET
import datetime
import psycopg2
import os
import eveLists
import connection
import simplejson


def LookupPrice(item, con):
    cur = con.cursor()
    cur.execute('SELECT price FROM PRICE_TEMP WHERE itemid = %s;', [item])
    answer = cur.fetchall()
    cur.close()
    if len(answer) > 0:
        #print('The lookup price answer is %s', answer[0][0])
        return answer[0][0]
    else:
        #print('the answer has length 0.')
        return 0


def CalculateProfit(system1, item1) :
    con = connection.establish_connection()
    cur = con.cursor()
    cur.execute('SELECT * FROM recipe WHERE ID = %s;', [item1])
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
            print("p1" + LookupPrice(p1,con))
            print("p2" + LookupPrice(p2, con))

            print()
            marginalCost = ((LookupPrice(p1, con)*q1 + LookupPrice(p2, con)*q2 + LookupPrice(p3, con)*q3) / q0)
            print("marginal cost: " + marginalCost)
            salePrice = LookupPrice(item1, con)
            marginalProfit = salePrice - marginalCost
            percentProfit = ((marginalProfit) * 100) / salePrice
            #print(item1, LookupPrice(item1, con),((LookupPrice(p1, con)*q1 + LookupPrice(p2, con)*q2 + LookupPrice(p3, con)*q3) / q0))
        except :
            marginalProfit = 0
            percentProfit = 0
            marginalCost = 0
            #print('zero division error, default to 0')
        #print(item1)
        cur.execute('UPDATE PRICE_TEMP SET PROFIT = %s, PROFITMARGIN = %s, COST = %s WHERE ITEMID = %s;', (
                                                                                                           marginalProfit,
                                                                                                           percentProfit,
                                                                                                           marginalCost,
                                                                                                           item1))
        con.commit()
        cur.close()
        con.close()

    else:
        try:
            marginalProfit = 0
            percentProfit = 0
            marginalCost = 0
            cur = con.cursor()
            #print('len(tempList) = 0')
            cur.execute("UPDATE PRICE_TEMP SET PROFIT = %s, PROFITMARGIN = %s, COST = %s WHERE ITEMID = %s;", (marginalProfit, percentProfit, marginalCost, item1))
            con.commit
            con.close()
        except:
            print('exception ')

def ClearTemp():
    con = connection.establish_connection()
    cur = con.cursor()
    cur.execute('TRUNCATE TABLE price_temp;')
    cur.close()
    con.commit()
    con.close()


###Main###
def main():
    print("Calculating Profit")
    for i in eveLists.systemList:
        ClearTemp()
        databaseName = eveLists.DatabaseDict[i]
    ###added after broke. need to repoppulate price_temp with system data
        con = connection.establish_connection()
        cur = con.cursor()
        cur.execute("INSERT INTO PRICE_TEMP SELECT * FROM {0};".format(databaseName))
        cur.close()
        con.commit()



        for j in eveLists.itemList:
            CalculateProfit(i, j)

        cur = con.cursor()
        cur.execute('UPDATE PRICE_TEMP SET PROFITMARGIN = 0, PROFIT = 0 WHERE PROFIT IS NULL;')
        cur.execute('UPDATE PRICE_TEMP SET COST = 0 WHERE COST IS NULL;')

        cur.execute('DROP TABLE {0};'.format(databaseName))
        cur.execute('CREATE TABLE {0} AS SELECT itemid,mysystem,price,profitmargin,mydate,mytime,profit,cost FROM PRICE_TEMP;'.format(databaseName))
        print("creating table {0}".format(i))
        cur.close()
        con.commit()
        con.close()
    print("calculateMargins complete")
    return 0

