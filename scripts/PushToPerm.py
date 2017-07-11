from urllib import parse, request
import xml.etree.ElementTree as ET
import datetime
import psycopg2
import os
import eveLists
import connection




def main():
    con = connection.establish_connection()
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM PERM_JITA")
    my_count = cur.fetchone()
    print("counting rowns: " + my_count )
    if my_count > 2250:
        cur.execute("DELETE (SELECT * FROM PERM_JITA ORDER BY mytime ASC LIMIT 500;  ) FROM PERM_JITA;")

    cur.execute("INSERT INTO PERM_JITA SELECT * FROM TEMP_JITA;")
    cur.execute("INSERT INTO PERM_AMARR SELECT * FROM TEMP_AMARR;")
    cur.execute("INSERT INTO PERM_RENS SELECT * FROM TEMP_RENS;")
    cur.execute("INSERT INTO PERM_DODIXIE SELECT * FROM TEMP_DODIXIE;")
    cur.close()
    con.commit()
    con.close()
    return 0

