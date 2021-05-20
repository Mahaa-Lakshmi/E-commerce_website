import sqlite3
db=sqlite3.connect('User.db')
cursor=db.cursor()
#cursor.execute("create table UserRegTable(name text,email text primary key,password text)")
#db.commit()
#cursor.execute("INSERT INTO UserRegTable(name,email,password) VALUES(?, ?, ?)",('mah','abc','12') )
'''cursor.execute("SELECT * FROM UserRegTable")
all_rows = cursor.fetchall()
db.commit()
for row in all_rows:
    print(row)
    
''''''
#productAvailability table
cursor.execute("create table ProductAvailTable(pid text primary key,pname text,price text,availability text,"
              "count text)")
#db.commit()

cursor.execute("INSERT INTO ProductAvailTable(pid,pname,price,availability,count) VALUES(?, ?, ?,?,?)",('1','Sea blue Shoe','Rs.400.00','Instock','100') )

cursor.execute("INSERT INTO ProductAvailTable(pid,pname,price,availability,count) VALUES(?, ?, ?,?,?)",('2','Sea blue Shoe','Rs.400.00','Instock','100') )
cursor.execute("INSERT INTO ProductAvailTable(pid,pname,price,availability,count) VALUES(?, ?, ?,?,?)",('3','Mens Fossil Watch','Rs.900.00','Instock','10') )
cursor.execute("INSERT INTO ProductAvailTable(pid,pname,price,availability,count) VALUES(?, ?, ?,?,?)",('4','Mens Round neck Tshirt blue','Rs.470.00','Instock','20') )
cursor.execute("INSERT INTO ProductAvailTable(pid,pname,price,availability,count) VALUES(?, ?, ?,?,?)",('5','Mens striped Tshirt','Rs.399.00','Instock','10') )
cursor.execute("INSERT INTO ProductAvailTable(pid,pname,price,availability,count) VALUES(?, ?, ?,?,?)",('6','Mens hoodie tshirt','Rs.600.00','Instock','10') )
cursor.execute("INSERT INTO ProductAvailTable(pid,pname,price,availability,count) VALUES(?, ?, ?,?,?)",('7','Mens Boot','Rs.700.00','Instock','40') )
cursor.execute("INSERT INTO ProductAvailTable(pid,pname,price,availability,count) VALUES(?, ?, ?,?,?)",('8','Mens Casual Shoe','Rs.480.00','Instock','30') )
'''
'''
#cursor.execute("ALTER TABLE ProductAvailTable DROP COLUMN pid")
'''
'''
cursor.execute("ALTER TABLE ProductAvailTable add column p_id int")

cursor.execute("INSERT INTO ProductAvailTable(p_id) VALUES(1)" )
cursor.execute("INSERT INTO ProductAvailTable(p_id) VALUES(2)" )
cursor.execute("INSERT INTO ProductAvailTable(p_id) VALUES(3)")
cursor.execute("INSERT INTO ProductAvailTable(p_id) VALUES(4)" )
cursor.execute("INSERT INTO ProductAvailTable(p_id) VALUES(5)" )
cursor.execute("INSERT INTO ProductAvailTable(p_id) VALUES(6)" )
cursor.execute("INSERT INTO ProductAvailTable(p_id) VALUES(7)" )
cursor.execute("INSERT INTO ProductAvailTable(p_id) VALUES(8)" )
''''''
cursor.execute("SELECT * FROM ProductAvailTable")
all_rows = cursor.fetchall()
#cursor.execute("DROP TABLE ProductAvailTable")
#print("Table dropped... ")
db.commit()

for row in all_rows:
   print(row)
'''

#orderstable

#cursor.execute("create table Orderstable(email text,product_id text,status text,quantity text)")
#db.commit()

#cursor.execute("drop table Orderstable")
# print("Table dropped... ")
#ALTER TABLE student ADD COLUMN Address varchar(32)
#cursor.execute("delete from Orderstable where email=?",[''])
#cursor.execute("ALTER TABLE Orderstable ADD COLUMN orderno text")
#cursor.execute('update Orderstable set status=? where email=? ',['Order Placed','siva@gmail.com'])
cursor.execute("INSERT INTO ProductAvailTable(pid,pname,price,availability,count) VALUES(?, ?, ?,?,?)",('9','Mens Black shirt','Rs.600.00','Instock','100') )


cursor.execute("SELECT * FROM ProductAvailTable")
all_rows = cursor.fetchall()
for row in all_rows:
   print(row)
db.commit()