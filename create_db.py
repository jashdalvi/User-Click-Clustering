import mysql.connector

db_conn = mysql.connector.connect(user='root', password='****',
                              host='127.0.0.1')

db_cursor = db_conn.cursor()

db_cursor.execute("CREATE DATABASE clicks")
# Using the clicks database
db_conn.database = "clicks"
# Creating the coordinates table
db_cursor.execute("CREATE TABLE coordinates (id INT AUTO_INCREMENT PRIMARY KEY, x FLOAT(5,4) NOT NULL, y FLOAT(5,4) NOT NULL)")

db_conn.commit()

db_cursor.close()
db_conn.close()