import pymysql

try:
    db=pymysql.connect(host="localhost",user='root',password='')
    cr=db.cursor()
    cr.execute("create database newinfo")
    print("database cteated!")
except Exception as e:
    print(e)

#create table

tbl_create="create table studinfo(id integer primary key auto_increment,name varchar(20),city varchar(50))"

try:
    db=pymysql.connect(host="localhost",user='root',password='',database="newinfo")
    cr.execute(tbl_create)
    print("create table!")
except Exception as e:
    print(e)

#Insert Data
"""insert_data="insert into studinfo(name,city)values('sanket','rajkot'),('nirav','surat'),('ashok','bhavnagar'),('hitesh','baroda'),('mahesh','ahmedabad')"

try:
    cr.execute(insert_data)
    db.commit()
    print("Record inserted!")
except Exception as e:
    print(e)"""

#Update Data
"""update_data="update studinfo set city='navsari' where id=4"
try:
    cr.execute(update_data)
    db.commit()
    print("Record updated!")
except Exception as e:
    print(e)"""

#Delete_Data
"""delete_data="delete from studinfo where id=5"
try:
    cr.execute(delete_data)
    db.commit()
    print("Record deleted!")
except Exception as e:
    print(e)"""
    
#Select Data
select_data="select * from studinfo"
try:
    cr.execute(select_data)
    data=cr.fetchall()
    #data=cr.fetchmany(3)
    #data=cr.fetchone()
    #print(data)
    
    for i in data:
        print(i)
except Exception as e:
    print(e)