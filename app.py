from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3 as sql
app=Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    con=sql.connect("db_web.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from users")
    data=cur.fetchall()
    return render_template("index.html",datas=data)

@app.route("/add_user",methods=['POST','GET'])
def add_user():
    if request.method=='POST':
        uname=request.form['uname']
        password=request.form['password']
        con=sql.connect("db_web.db")
        cur=con.cursor()
        cur.execute("insert into users(UNAME,PASSWORD) values (?,?)",(uname,password))
        con.commit()
        flash('User Added','success')
        return redirect(url_for("index"))
    
    return render_template("add_user.html")

@app.route("/edit_user/<string:uid>",methods=['POST','GET'])
def edit_user(uid):
    if request.method=='POST':
        uname=request.form['uname']
        password=request.form['password']
        con=sql.connect("db_web.db")
        cur=con.cursor()
        cur.execute("update users set UNAME=?, PASSWORD=? where UID=?",(uname,password,uid))
        con.commit()
        flash('User updated','success')
        return redirect(url_for("index"))
    
    con=sql.connect("db_web.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from users where UID=?",(uid,))
    data=cur.fetchone()
    return render_template("edit_user.html",datas=data)



@app.route("/detet_user/<string:uid>",methods=['GET'])
def delete_user(uid):
    con=sql.connect("db_web.db")
    cur=con.cursor()
    cur.execute("delete from users where UID=?", (uid,))
    con.commit()
    flash('User Deleted','Warning')
    return redirect(url_for("index"))


if __name__=='__main__':
    app.secret_key='admin123'
    app.run(debug=True)
