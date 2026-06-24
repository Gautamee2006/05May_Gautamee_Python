import sqlite3

try:
    db=sqlite3.connect("demo.db")
    print("Database connected/created!")
except Exception as e:
    print(e)

#table create

tbl_create="create table studinfo(id integer primary key autoincrement,name varchar(20),city varchar(50))"

try:
    db.execute(tbl_create)
    print("create table!")
except Exception as e:
    print(e)

#insert data

'''tbl_insert="insert into studinfo(name,city)values('gautamee','rajkot'),('riya','rajkot'),('hetvi','rajkot'),('rajavi','rajkot'),('hinali','rajkot')"

try:
    db.execute(tbl_insert)
    db.commit()
    print("record insert!")
except Exception as e:
    print(e)'''

#update data

'''tbl_update="update studinfo set city='surat' where id=3 "

try:
    db.execute(tbl_update)
    db.commit()
    print("record update!")
except Exception as e:
    print(e)'''

#delete data

'''tbl_delete="delete from studinfo where id='5'"

try:
    db.execute(tbl_delete)
    db.commit()
    print("record delete!")
except Exception as e:
    print(e)'''

#select data
cr=db.cursor()
tbl_select="select *from studinfo"

try:
    cr.execute(tbl_select)
    data=cr.fetchall()
    #data=cr.fetchmany(3)
    #data=cr.fetchone()
    #print(data)
    for i in data:
        print(i)
except Exception as e:
    print(e)