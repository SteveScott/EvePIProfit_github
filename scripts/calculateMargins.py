from urllib2 import Request, urlopen, URLError
import xml.etree.ElementTree as ET
import datetime
import psycopg2
import os
import urlparse
import eveLists

os.environ['DATABASE_URL']='postgres://lojyjajvpwaaci:4ya_0u6olTZ2taL68me6Goa1HD@ec2-54-243-199-161.compute-1.amazonaws.com:5432/deaek2i6u7a13g'

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

con = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

def LookupPrice(item):
    cur = con.cursor()
    cur.execute('SELECT PRICE FROM PRICE_TEMP WHERE ITEMID = %s', [item])
    answer = cur.fetchall()
    cur.close()
    if len(answer) > 0:
        return answer[0][0]
    else:
        return 0

def CalculateProfit(system1, item1) :

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
    cur.close

    if len(tempList) > 0:
        try:
            netCost = ((LookupPrice(p1)*q1 + LookupPrice(p2)*q2 + LookupPrice(p3)*q3) / q0)
            salePrice = LookupPrice(item1)
            netProfit = salePrice - netCost
            percentProfit = ((salePrice - netCost) * 100) / netCost
            print item1, LookupPrice(item1),((LookupPrice(p1)*q1 + LookupPrice(p2)*q2 + LookupPrice(p3)*q3) / q0)
        except ZeroDivisionError:
            netProfit = 0
            percentProfit = 0
            print('zero division error, default to 0')
        cur = con.cursor()
        print item1
        cur.execute('UPDATE PRICE_TEMP SET PROFIT = %s, PROFITMARGIN = %s WHERE ITEMID = %s', (netProfit, percentProfit, item1))
        con.commit()
        cur.close()

    else:
        print('0')

def ClearTemp():
    cur = con.cursor()
    cur.execute('TRUNCATE TABLE price_temp')
    cur.close()
    con.commit()


###Main###
for i in eveLists.systemList:
    ClearTemp()
    databaseName = eveLists.DatabaseDict[i]
###added after broke. need to repoppulate price_temp with system data
    cur=con.cursor()
    cur.execute("INSERT INTO PRICE_TEMP SELECT * FROM {0};".format(databaseName))
    cur.close()

####
    for j in eveLists.itemList:
        CalculateProfit(i, j)

'''
#instead of deleting and re-adding the table, let's modify the existing table
#below is the delete and re-add code
    cur = con.cursor()
    cur.execute('DROP TABLE {0}'.format(databaseName))
    cur.execute('CREATE TABLE {0} AS SELECT itemid, mysystem, price, profitmargin,mydate,mytime,profit FROM price_temp'.format(databaseName))
    cur.close()
'''
if con:
    con.commit()