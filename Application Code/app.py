from flask import Flask, render_template, url_for, flash, redirect
import pandas as pd
import requests
from flask import request
import spacy
import json
import csv


nlp = spacy.load("en_core_web_sm")
username = 670

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def hello():
	return render_template('login.html')

@app.route('/auth', methods=['POST'])
def auth():
	global username
	username = request.form['username']
	password = request.form['password']
	login = False

	with open('testing/db_dell.csv', 'r') as csvfile:
		csv_reader = csv.reader(csvfile)

		for row in csv_reader:
			if row[0]== username and row[15] == password:
				login = True
				break

	if login == True:
		print("You are now logged in!")
		return redirect(url_for('data'))
	else:
		flash('Wrong Username or Password!')
		return redirect(url_for('hello'))


@app.route('/query', methods=['GET','POST'])
def data():
	return render_template("index.html")

@app.route('/status', methods=['GET','POST'])
def status():
	data = pd.read_csv (r'testing/db_dell.csv', delimiter=",")
	user_ID = request.form['data']
	doc = nlp(user_ID)
	ID = int(username)
	print(ID)

	arr=["Emp ID"]

	for token in doc:
		if(token.lemma_=="department"):
				arr.append("Emp_dept")
		elif(token.lemma_=="date"):
			if(token.nbor(-1).text=="expected"):
				arr.append("Expected Date")
			elif(token.nbor(-1).text=="order"):
				arr.append("Order date")
		elif(token.lemma_=="shipment"):
			arr.append("Shipment Status")
		elif(token.lemma_=="order"):
			if(token.nbor().text=="number"):
				arr.append("Order no.")
			elif(token.nbor().text=="stock"):
				arr.append("Order stock")
		elif(token.lemma_=="city"):
			if(token.nbor().text=="manufactured"):
				arr.append("City manufactured")
			elif(token.nbor().text=="delivered"):
				arr.append("City delivery")
		elif(token.lemma_=="product"):
			if(token.nbor().text=="price"):
				arr.append("Product price")
			elif(token.nbor().text=="category"):
				arr.append("Product category")
			elif(token.nbor().text=="name"):
				arr.append("Product name")
		elif(token.lemma_=="quantity"):
			arr.append("Quantity")


	df = pd.DataFrame(data, columns = arr)
	df.set_index("Emp ID", inplace = True)
	result = df.loc[ID]
	result = result.to_json()
	result = json.loads(result)
	print(result)
	print("\n")

	return result

@app.route('/logout')
def logout():
	return redirect(url_for('hello'))


if __name__ == '__main__':
	try:
		app.run('localhost', port = 5000, debug = True, use_reloader = True)
	except Exception as e:
		print (e)
