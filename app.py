# -*- coding: utf-8 -*-
"""
Created on Mon May 24 08:10:31 2021

@author: liyae
"""

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
app = Flask(__name__)

app.secret_key = 'a'

app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'CRc6DD2VYo'
app.config['MYSQL_PASSWORD'] = 'lwN3aYDMDo'
app.config['MYSQL_DB'] = 'CRc6DD2VYo'
mysql = MySQL(app)

@app.route('/')
def home() :
    return render_template('home.html')

@app.route('/adminlogin', methods =['GET', 'POST'])
def adminlogin():
    global userid
    msg= ''
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = % s AND password = % s', (username,password), )
        account = cursor.fetchone()
        print(account)
        if account :
            session['loggedin'] = True
            session['id'] = account[0]
            userid = account[0]
            session['username'] = account[1]
            msg="Logged in successfully !!"
            return render_template('admindashboard.html', msg=msg)
        else:
            msg="Incorrect username/password"
    return render_template('adminlogin.html', msg = msg)

@app.route('/admindashboard')
def dash():
    return render_template('admindashboard.html')


@app.route('/addnewadmin',methods = ['GET','POST'])
def addnewadmin():
    msg=''
    if request.method == 'POST':
        name = request.form['name'] 
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = % s', (username, ))
        account = cursor.fetchone()
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO admin VALUES (NULL, % s, % s, % s,% s)', (name, email,username, password),)
            mysql.connection.commit()
            msg = 'Added new admin successfully !'
            
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('addnewadmin.html', msg = msg)

@app.route('/userregistration',methods = ['GET','POST'])
def userregistration():
    msg=''
    if request.method == 'POST':
        name = request.form['name'] 
        email = request.form['email']
        location = request.form['location']
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username = % s', (username, ))
        account = cursor.fetchone()
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s,% s, % s, % s,% s)', (name, email,location,username, password),)
            mysql.connection.commit()
            msg = 'You are successfully registered !'
            
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('userregistration.html', msg = msg)

@app.route('/userlogin', methods =['GET', 'POST'])
def userlogin():
    global userid
    msg= ''
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username = % s AND password = % s', (username,password), )
        account = cursor.fetchone()
        print(account)
        if account :
            session['loggedin'] = True
            session['id'] = account[0]
            userid = account[0]
            session['username'] = account[1]
            msg="Logged in successfully !!"
            return render_template('userdashboard.html', msg=msg)
        else:
            msg="Incorrect username/password"
    return render_template('userlogin.html', msg = msg)

@app.route('/addcontainment',methods = ['GET','POST'])
def addcontainment():
    msg=''
    if request.method == 'POST':
        location = request.form['location']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM location WHERE location = % s', (location, ))
        account = cursor.fetchone()
        print(account)
        if account:
            msg = 'This place is already a containment zone !'
        else:
            cursor.execute('INSERT INTO location VALUES (NULL, % s)', (location,))
            mysql.connection.commit()
            msg = 'The place is successfully added !'
            
 
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('addcontainment.html', msg = msg)

@app.route('/seepeople',methods = ['GET','POST'])
def seepeople():
    msg=''
    if request.method == 'POST':
        location = request.form['location']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE location = % s', (location, ))
        account = cursor.fetchone()
        print(account)
        if account :
           print("People List",account)
           return render_template('seepeople.html', msg = account)

        else:
           msg = ' No people in this locality'
    elif request.method == 'POST':
        msg = '  No people in this locality!'
    return render_template('seepeople.html', msg = msg)

@app.route('/userdashboard')
def dashboard():
    return render_template('userdashboard.html')

@app.route('/checklocation',methods = ['GET','POST'])
def checklocation():
    msg=''
    if request.method == 'POST':
        location = request.form['location']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM location WHERE location = % s', (location, ))
        account = cursor.fetchone()
        print(account)
        if account :
           msg='The location is a containment zone'
        else:
           msg = ' Not a containment zone'
    elif request.method == 'POST':
        msg = '  Not a containment zone'
    return render_template('checklocation.html', msg = msg)


        
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return render_template('home.html')
    
if __name__ == '__main__' :
    app.run( host = '0.0.0.0' ,debug = True, port = 5000)
