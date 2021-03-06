from urllib import request, error, parse
import xml.etree.ElementTree as ET
import datetime
import psycopg2
import os
import eveLists
import connection

con = connection.establish_connection()
cur = con.cursor()

def LookupPrice(item):

    cur.execute('SELECT price FROM PRICE_TEMP WHERE itemid = %s;', [item])
    answer = cur.fetchall()

    if len(answer) > 0:
        #print('The lookup price answer is %s', answer[0][0])
        return answer[0][0]
    else:
        #print('the answer has length 0.')
        return 0


def CalculateProfit(system1, item1):
    global cur
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
        p0 = LookupPrice(i0)
        p1 = LookupPrice(i1)
        p2 = LookupPrice(i2)
        p3 = LookupPrice(i3)

    #produced = # [tempList[1]


        if ((p0 == 0) or (q1 > 0 and p1 == 0) or (q2 > 0 and p2 == 0) or (q3 > 0 and p3 == 0)):
            print(str(i0) + " no price found for one of the commodities")

            marginalProfit = 0
            percentProfit = 0
            marginalCost = 0

        else:

            marginalCost = (p1 * q1 + p2 * q2 + p3 * q3) / q0
            salePrice = LookupPrice(item1)
            marginalProfit = salePrice - marginalCost
            percentProfit = ((marginalProfit) * 100) / salePrice

        print("updating", i0, p0, p1, q1, p2, q2, p3, q3)
        cur.execute('UPDATE PRICE_TEMP SET PROFIT = %s, PROFITMARGIN = %s, COST = %s WHERE ITEMID = %s;', (marginalProfit, percentProfit, marginalCost, item1))
        con.commit()


    else:
        try:
            marginalProfit = 0
            percentProfit = 0
            marginalCost = 0
            cur = con.cursor()
            #print('len(tempList) = 0')
            cur.execute("UPDATE PRICE_TEMP SET PROFIT = %s, PROFITMARGIN = %s, COST = %s WHERE ITEMID = %s;", (marginalProfit, percentProfit, marginalCost, item1))

        except:
            print('exception ')

def ClearTemp():
    global cur
    print("truncating table price_temp")
    cur.execute('TRUNCATE TABLE price_temp')
    con.commit()
    #print("price_temp truncated")



###Main###
def main():
    print("Calculating Profit")
    for i in eveLists.systemList:
        ClearTemp()
        databaseName = eveLists.databaseDict[i]
    ###added after broke. need to repoppulate price_temp with system data

        cur.execute("INSERT INTO PRICE_TEMP SELECT * FROM {0};".format(databaseName))
        con.commit()



        for j in eveLists.itemList:
            CalculateProfit(i, j)


        cur.execute('UPDATE PRICE_TEMP SET PROFITMARGIN = 0, PROFIT = 0 WHERE PROFIT IS NULL;')
        cur.execute('UPDATE PRICE_TEMP SET COST = 0 WHERE COST IS NULL;')

        cur.execute('DROP TABLE {0};'.format(databaseName))
        cur.execute('CREATE TABLE {0} AS SELECT itemid,mysystem,price,profitmargin,mydate,mytime,profit,cost FROM PRICE_TEMP;'.format(databaseName))
        print("creating table {0}".format(eveLists.databaseDict[i]))
    cur.close()
    con.commit()
    con.close()
    print("calculateMargins complete")
    return 0

