# code by Liam Beaver
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="myusername",
  password="mypassword"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE newdatabase")

mycursor.execute("SHOW DATABASES")

for x in mycursor:
  print(x)

mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")
