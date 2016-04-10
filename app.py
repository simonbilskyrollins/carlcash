# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session
import os
import scraper
import json
import time

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
	dining_dollars = "$" +  parseJSON["dining_dollars"]
	schillers = "$" +  parseJSON["schillers"]
	guest_swipes = parseJSON["guest_meals"]
	meals_left = parseJSON["meals_week"]
	
	temp = 0
	if guest_swipes > 3:
		temp = meals_left
		meals_left = guest_swipes
		guest_swipes = temp
	
	spending = parseJSON["spending"]
	swipes = parseJSON["swipes"]
	week, diningDollarBudget, laundryLeft, LDCCardSwipes, burtonCardSwipes = getASI(parseJSON)
	
	return render_template('index.html', dining=dining_dollars, meals=meals_left, schill=schillers, guest=guest_swipes, spending=spending, swipes=swipes, laundry=laundryLeft, diningBudget=diningDollarBudget, ldc=LDCCardSwipes, burton=burtonCardSwipes)

def getASI(parseJSON):
	dining_dollars = float(parseJSON["dining_dollars"])
	schillers = float(parseJSON["schillers"])
	swipes = parseJSON["swipes"]
	
	week = getWeek()
	diningDollars = diningDollarBudget(dining_dollars, week)
	laundryLoadsLeft = laundryLeft(schillers)
	LDCCardSwipes, burtonCardSwipes = LDCBurtonSwipes(swipes)
	
	return week, diningDollars, laundryLoadsLeft, LDCCardSwipes, burtonCardSwipes

def diningDollarBudget(dollarsLeft, week):
    return "$" + str(round(dollarsLeft/(10-week), 2))

def laundryLeft(schillersLeft):
    return int(schillersLeft/2.25)
    
def LDCBurtonSwipes(swipes):
    LDCCount=0
    BurtonCount=0
    
    for key in swipes:
    	if "LDC" in swipes[key]["location"]:
    		LDCCount += 1
    	else:
    		BurtonCount += 1
    		
    return LDCCount, BurtonCount

def getWeek():
	month = int(time.strftime("%m"))
	day = int(time.strftime("%d"))
	week = 0
	if ((month==3) and (28<=day) or (month==4) and (day<=3)):
		week=1
	elif ((month==4) and (4<=day) and (day<=10)):
		week=2
	elif ((month==4) and (11<=day) and (day<=17)):
		week=3
	elif ((month==4) and (18<=day) and (day<=24)):
		week=4
	elif ((month==4) and (25<=day) or (month==5) and (day<=1)):
		week=5
	elif ((month==5) and (2<=day) and (day<=8)):
		week=6
	elif ((month==5) and (9<=day) and (day<=15)):
		week=7
	elif ((month==5) and (16<=day) and (day<=22)):
		week=8
	elif ((month==5) and (23<=day) and (day<=29)):
		week=9
	elif ((month==5) and (30<=day) or (month==6) and (day<=7)):
		week=10
	print week
	return week
	
# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)