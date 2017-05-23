from scripts import connection
import psycopg2

con = connection.establish_connection()
cur = con.cursor()
try:
    cur.execute("TRUNCATE TABLE temp_jita;")
except:
    print("could not truncate temp_jita")
cur.close()
con.close()