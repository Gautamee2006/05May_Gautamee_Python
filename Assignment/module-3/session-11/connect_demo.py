'''Install the pymysql package in your Python environment and write a script connect_demo.py 
that connects to a local MySQL server using your credentials and prints 'Connection successful'
 if the connection is established.'''

import pymysql

try:
    connection = pymysql.connect(
        host="localhost",
        user="root",        
        password="",
        database="demo"      
    )

    print("Connection successful")

    connection.close()

except pymysql.MySQLError as e:
    print("Connection failed")
    print("Error:", e)