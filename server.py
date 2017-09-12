from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector

import md5 # imports the md5 module to generate a hash
import os, binascii # include this at the top of your file
salt = binascii.b2a_hex(os.urandom(15))

app = Flask(__name__)
mysql = MySQLConnector(app,'friendsdb')

@app.route('/')
def index():
	query = "SELECT * FROM friends"                           # define your query
	friends = mysql.query_db(query)
	# password = 'password'                 # run query with query_db()
	# hashed_password = md5.new(password).hexdigest()
	#print hashed_password, "this si the hash" #this will show you the hashed value
	# 5f4dcc3b5aa765d61d8327deb882cf99 -> nice!
	return render_template('index.html', all_friends=friends)

@app.route('/friends', methods=['POST'])
def create():
    # add a friend to the database!
	first_name = request.form['first_name'].strip()
	last_name = request.form['last_name'].strip()
	occupation = request.form['occupation'].strip()
	age = request.form['age'].strip()	
	friendsince = request.form['friendsince'].strip()	

	query = 'INSERT INTO friends(first_name, last_name, occupation, age, friendsince) VALUES (:first_name, :last_name, :occupation, :age, :friendsince)'
	data = {'first_name': first_name, 'last_name': last_name, 'occupation': occupation, 'age': age, 'friendsince': friendsince}
	friends = mysql.query_db(query, data)
	return redirect('/')

@app.route('/friends/<friend_id>')
def show(friend_id):
    # Write query to select specific user by id. At every point where
    # we want to insert data, we write ":" and variable name.
    query = "SELECT * FROM friends WHERE id = :specific_id"
    # Then define a dictionary with key that matches :variable_name in query.
    data = {'specific_id': friend_id}
    # Run query with inserted data.
    friends = mysql.query_db(query, data)
    # Friends should be a list with a single object,
    # so we pass the value at [0] to our template under alias one_friend.
    return render_template('index.html', one_friend=friends[0])
app.run(debug=True)