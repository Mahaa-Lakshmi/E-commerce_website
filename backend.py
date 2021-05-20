from flask import Flask, render_template, request, url_for,redirect
import sqlite3 as sql
import re
import string
import random


app = Flask(__name__)
activeuser=""
nelist=[]


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/homepage')
def homepage():
    con = sql.connect("User.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from ProductAvailTable")
    items = cur.fetchall()
    return render_template("home.html", items=items)
    con.close()

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
            #con = sql.connect("User.db")
            #con.row_factory = sql.Row
            #cur = con.cursor()

            uname = request.form['username']
            global activeuser
            activeuser=uname
            pwd = request.form['password']
            with sql.connect("User.db") as con:
                cur = con.cursor()
                params=(uname,pwd)
                #query = "SELECT email,password FROM UserRegTable where email="+uname+" and password="+pwd
                #cur.execute('SELECT email,password FROM DBtable WHERE email=? and password=?', (uname,pwd))
                checkUsername = cur.execute('SELECT * FROM UserRegTable WHERE email=? and password=?', (uname,pwd))
                #checkUsername=cur.execute(query)
                checkUsername=checkUsername.fetchall()
                if len(checkUsername)>0:
                    cur.execute("select * from ProductAvailTable")
                    items = cur.fetchall()
                    return render_template("home.html", items=items)
                    con.close()


                else:
                   # con.rollback()

                    return render_template("index.html",row="Username or password not found")

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            with sql.connect("User.db") as con:
                cur = con.cursor()

                cur.execute("INSERT INTO UserRegTable(name,email,password) VALUES(?, ?, ?)",
                            (name, email, password))

                con.commit()
                msg = "Record successfully added.Please login to proceed"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("index.html",msg=msg)
            con.close()

@app.route('/view<id>', methods=['POST', 'GET'])
def view(id):
    con = sql.connect("User.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('SELECT * FROM ProductAvailTable WHERE pid=?',id)
    rows = list(cur.fetchone())
    rows.append("Add to Cart")
    return render_template("product_details.html",rows=rows)
    con.close()





@app.route('/addToCart<id>', methods=['POST', 'GET'])
def addToCart(id):
    global activeuser
    con = sql.connect("User.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    quantity=request.form['quantity']
    cur.execute('select count from ProductAvailTable where pid=?',[id])
    quant_check=cur.fetchone()
    if int(quantity)<int(quant_check[0]):
        cur.execute("INSERT INTO Orderstable(email,product_id,status,quantity) VALUES(?, ?, ?,?)",
                (activeuser,id,'cart',quantity))
    con.commit()
    cur.execute('SELECT * FROM ProductAvailTable WHERE pid=?', id)
    rows = list(cur.fetchone())
    rows.append("Added")
    return render_template("product_details.html", rows=rows)
    con.close()


@app.route('/Cartpage', methods=['POST', 'GET'])
def Cartpage():
    global activeuser
    quants=[]
    con = sql.connect("User.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('select * from ProductAvailTable where pid in(SELECT product_id FROM Orderstable WHERE email=? and status=?)',[activeuser,'cart'])
    rows = cur.fetchall()
    for row in rows:
        cur.execute('select quantity from Orderstable where product_id=? and email=?', [row[0], activeuser])
        elem = cur.fetchall()
        quants.extend([float(elem1[0]) for elem1 in elem])
    return render_template("cart.html",rows=rows,quants=quants)
    con.close()

@app.route('/Checkoutpage', methods=['POST', 'GET'])
def Checkoutpage():
    global activeuser
    global nelist
    con = sql.connect("User.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    if len(nelist)>0:
        res = ''.join(random.choices(string.ascii_uppercase +string.digits, k=10))
    else:
        res=''
    cur.execute('select * from ProductAvailTable where pid in(SELECT product_id FROM Orderstable WHERE email=? and '
                'status=?)',[activeuser,'cart'])
    rows = list(cur.fetchall())
    con.commit()

    quants=[]
    res=0
    for row in rows:
        cur.execute('select quantity from Orderstable where product_id=? and email=? and status=?',[row[0],activeuser,'cart'])
        elem=cur.fetchall()
        quants.extend([float(elem1[0]) for elem1 in elem])
        nelist.extend([float(re.findall("[+-]?\d+\.\d+",row[2])[0])*float(elem1[0]) for elem1 in elem ])


    con.commit()
    res=sum(nelist)
    rows.append(res)
    rows.append(res+20)
    print(nelist)
    return render_template("checkout.html",rows=rows,quants=quants)
    con.close()

@app.route('/OrderPlaced', methods=['POST', 'GET'])
def OrderPlaced():
    global activeuser
    global nelist
    quants=[]
    list_rows=[[]]
    if len(nelist)>0:
        res = ''.join(random.choices(string.ascii_uppercase +string.digits, k=10))
    else:
        res=''

    con = sql.connect("User.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    orderprice=""


    cur.execute('select * from ProductAvailTable where pid in(SELECT product_id FROM Orderstable WHERE email=?)',
                [activeuser])
    rows = list(cur.fetchall())
    print(nelist)
    if len(nelist)>0:
        i=0
        for row in rows:
            cur.execute('select count from ProductAvailTable where pid=?', row[0])
            quant_check = cur.fetchone()
            if i<len(nelist):
                cur.execute('update Orderstable set status=?,orderno=?,orderedprice=? where product_id=? and email=? and status=?',["Order Placed",res,nelist[i],row[0],activeuser,'cart'])
                i+=1
                cur.execute('select quantity from Orderstable where product_id=? and status=?', [row[0],'Order Placed'])
                quant_ordered = cur.fetchone()
                cur.execute('update ProductAvailTable set count=? where pid=?',
                            [int(quant_check[0]) - int(quant_ordered[0]), row[0]])

            else:
                cur.execute('update Orderstable set status=?,orderno=? where product_id=? and email=? and status=?',
                            ["Order Placed", res, row[0], activeuser,'cart'])
                cur.execute('select quantity from Orderstable where product_id=? and status=?', [row[0], 'Order Placed'])
                quant_ordered = cur.fetchone()
                cur.execute('update ProductAvailTable set count=? where pid=?',
                            [int(quant_check[0]) - int(quant_ordered[0]), row[0]])

        cur.execute('select orderedprice,orderno from Orderstable where status=? and email=? and product_id=?',
                    ['Order Placed', activeuser])
        orderprice = cur.fetchall()
        con.commit()




    #Checkoutpage()
    return render_template("orders..html",rows=rows,nelist=nelist,orderprice=orderprice)

    con.close()


if __name__ == '__main__':
    app.run(debug=True)