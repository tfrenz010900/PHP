import MySQLdb
import sys

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="smartmitt",         # your username
                     passwd="smartmitt",  # your password
                     db="smartmitt")        # name of the data base

# create a Cursor object.
cur = db.cursor()

# Use all the SQL you like
cur.execute("INSERT INTO system_logs (AccountID, column2, column3) VALUES (sys.argv[1], sys.argv[2], sys.argv[3]);")


db.close()
