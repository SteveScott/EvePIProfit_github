from scripts import connection
import psycopg2

con = connection.establish_connection()
cur = con.cursor()
cur.execute("select * from temp_jita;")
print(cur.fetchall())
cur.close()
con.close()