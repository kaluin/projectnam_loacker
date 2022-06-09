import manageDB
from time import sleep
def post():
    sql="SELECT isNeverConnected FROM locker_info;"
    manageDB.cur.execute(sql)
    sleep(1)
    sql="SELECT * FROM locker_info;"
    manageDB.cur.execute(sql)
    result=manageDB.cur.fetchall()
    return result[0]
def set(NAME, VALUE):
    if type(VALUE) is int:
        sql="UPDATE locker_info SET "+NAME+"="+str(VALUE)+" WHERE lockername='SungkyulLocker_A';"
    else:
        sql="UPDATE locker_info SET "+NAME+"='"+VALUE+"' WHERE lockername='SungkyulLocker_A';"
    manageDB.cur.execute(sql)
    manageDB.conn.commit()
def get(NAME):
    sql="SELECT "+NAME+" FROM locker_info;"
    manageDB.cur.execute(sql)
    result = manageDB.cur.fetchall()
    return result[0][0]
    
