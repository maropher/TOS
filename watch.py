from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3 as sql
app = Flask(__name__)
app.secret_key = 'kappa123'
@app.route('/')
def home():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("select * from watch")
   rows = cur.fetchall()
   return render_template('home.html',rows = rows)

@app.route('/login')
def login():
   return render_template('login.html')

@app.route('/register')
def register():
   return render_template('signup.html')

@app.route('/signin',methods = ['POST'])
def signin():
   if request.method == 'POST':
         email = request.form['email']
         pwd = request.form['pwd']
         success = '0'
         con = sql.connect("database.db")
         con.row_factory = sql.Row
         cur = con.cursor()
         cur.execute("select * from users")
         rows = cur.fetchall()
         for row in rows:
             if row["email"] == email and row["password"] == pwd and success == '0':
                 success = '1'
                 session['username'] = email

         if success == '1':
             return redirect(url_for('home'))
         else:
             return "Invalid"

@app.route('/addwatch')
def addwatch():
   return render_template('addwatch.html')

@app.route('/insertwatch',methods = ['POST'])
def insertwatch():
   name = request.form['postName']
   desc = request.form['postDescription']
   url = request.form['postImageUrl']
   star = request.form['postStar']
   price = request.form['postPrice']
   con = sql.connect("database.db")
   cur = con.cursor()
   cur.execute("INSERT INTO watch (watchId,name,description,imageUrl,star,price) VALUES (NULL,?,?,?,?,?)",(name,desc,url,star,price))
   con.commit()
   return redirect(url_for('home'))

@app.route('/buynow',methods = ['POST'])
def buynow():
   hid = request.form['watch_id']
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("select * from users where email=?",(session['username'],))
   rows = cur.fetchall()
   for row in rows:
      uid = row["userId"]
   con.close()
   conn = sql.connect("database.db")
   cur = conn.cursor()
   cur.execute("INSERT INTO cart (cartId,watchId,userId) VALUES (NULL,?,?)", (hid,uid))
   conn.commit()
   return redirect(url_for('home'))

@app.route('/deletebookings',methods = ['POST'])
def deletebookings():
   hid = request.form['watch_id']
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("select * from users where email=?",(session['username'],))
   rows = cur.fetchall()
   for row in rows:
      uid = row["userId"]
   con.close()
   conn = sql.connect("database.db")
   cur = conn.cursor()
   cur.execute("DELETE from cart where watchId=? and userId=?", (hid,uid))
   conn.commit()
   return redirect(url_for('mycart'))

@app.route('/deleteproducts',methods= ['POST'])
def deleteproducts():
   wid = request.form['product_id']
   con = sql.connect("database.db")
   cur = con.cursor()
   cur.execute("DELETE from watch where watchId=?", (wid))
   con.commit()
   return redirect(url_for('home')) 

@app.route('/editproducts',methods= ['POST'])
def editproducts():
   wid = request.form['pid']
   desc = request.form['desc']
   nama = request.form['pname']
   pr = request.form['price']
   image = request.form['imageURL']
   con = sql.connect("database.db")
   cur = con.cursor()
   cur.execute("UPDATE watch SET name='%s', description='%s', imageUrl='%s', price='%s'  WHERE watchId=%s " %(nama,desc,image,pr,wid)) 
   con.commit()
   return redirect(url_for('home'))

@app.route('/watchdetails',methods = ['GET'])
def watchdetails():
   id = request.args.get('id')
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("select * from watch where watchId=?",(id,))
   rows = cur.fetchall()
   return render_template('watch-detail.html',rows = rows)

@app.route('/edit',methods = ['POST'])
def edit():
   id = request.form['product_id']
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("select * from watch where watchId=?", (id,))
   rows = cur.fetchall()
   return render_template('edit.html',rows=rows)

@app.route('/mycart')
def mycart():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("select * from users where email=?",(session['username'],))
   rows = cur.fetchall()
   for row in rows:
      uid = row["userId"]
   con.close()
   conn = sql.connect("database.db")
   conn.row_factory = sql.Row
   cur = conn.cursor()
   cur.execute("select * from watch inner join cart on watch.watchId=cart.watchId where cart.userId=?",(uid,))
   rows = cur.fetchall()
   return render_template('mycart.html',rows = rows)

@app.route('/signup',methods = ['POST'])
def signup():
   if request.method == 'POST':
         email = request.form['email']
         pwd = request.form['pwd']
	 nama = request.form['nama']
	 notelp = request.form['notelp']
         success = 0
         con = sql.connect("database.db")
         cur = con.cursor()
         cur.execute("INSERT INTO users (userId,email,nama,nomor,password) VALUES (NULL,?,?,?,?)",(email,nama,notelp,pwd))
         con.commit()
         return redirect(url_for('home'))

@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('home'))

if __name__ == '__main__':
   app.debug = True
   app.run('0.0.0.0',5220)
