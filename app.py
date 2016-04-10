# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session
import os
import scraper
import json

# create the application object
app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
	form = request.form
	form_un = form['username']
	form_pw = form['password']
	mylist = [form_un, form_pw]
	session['mylist'] = mylist
        return redirect(url_for('home'))

    return render_template('login.html', error = error)

@app.route('/index.html')
def home():
    infoList = ['', '']
    j = 0
    for i in session.pop('mylist', []):
	infoList[j] = i	
	j += 1
    JSON = scraper.main(infoList[0], infoList[1])
    parseJSON = json.loads(JSON)
    dining_dollars = parseJSON["dining_dollars"]
    schillers = parseJSON["schillers"]
    guest_swipes = parseJSON["guest_meals"]
    meals_left = parseJSON["meals_week"]
    return render_template('index.html', dining=dining_dollars, meals=meals_left, schill=schillers, guest=guest_swipes)

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
