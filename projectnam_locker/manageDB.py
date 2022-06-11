from sys import exit
from mariadb import connect, Error

try:
    conn = connect(user="root",password="****",host="127.0.0.1",port=3306,database="projectnam")
except Error as e:
    print("Error Connecting to MariaDB Platform")
    exit(1)
    
cur = conn.cursor()
