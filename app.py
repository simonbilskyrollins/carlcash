# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session
import os
import scraper
import json
import time
import datetime

# create the application object
app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        form = request.form
        form_un = form['username']
        form_pw = form['password']
        mylist = [form_un, form_pw]
        session['mylist'] = mylist
        return redirect(url_for('home'))

    return render_template('login.html', error=error)


@app.route('/index.html')
def home():
    infoList = ['', '']
    j = 0
    for i in session.pop('mylist', []):
        infoList[j] = i 
        j += 1

    JSON, dining_transactions, schiller_transactions = scraper.main(infoList[0], infoList[1])

    if not JSON:
	return redirect(url_for('login'))

    parseJSON = json.loads(JSON)

    dining_dollars = parseJSON["dining_dollars"]
    schillers = parseJSON["schillers"]
    guest_swipes = parseJSON["guest_meals"]
    if 'meals_week' in parseJSON:
	meals_left = parseJSON["meals_week"]
    else:
 	meals_left = ''
    json_obj = JSON

    temp = 0
    
    if int(guest_swipes) > 3:
        temp = meals_left
        meals_left = guest_swipes
        guest_swipes = temp

    if 'spending' in parseJSON:
    	spending = parseJSON["spending"]
    else:
	spending = ''

	dining_transactions = "[{day: '%s', balance: %s}, {day: '%s', balance: %s}]" % (datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=-1), '%Y-%m-%d %H:%M'), dining_dollars, time.strftime('%Y-%m-%d %H:%M'), dining_dollars)

	schiller_transactions = "[{day: '%s', balance: %s}, {day: '%s', balance: %s}]" % (datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=-1), '%Y-%m-%d %H:%M'), schillers, time.strftime('%Y-%m-%d %H:%M'), schillers)
	 
 
    if 'swipes' in parseJSON:
    	swipes = parseJSON["swipes"]
    else:
	swipes = ''

    week, diningDollarBudget, dailyDiningBudget, laundryLeft, LDCCardSwipes, burtonCardSwipes = getASI(parseJSON)

    return render_template('index.html', dining= "$" + dining_dollars, meals=meals_left, schill="$" + schillers, guest=guest_swipes, spending=spending, swipes=swipes, laundry=laundryLeft, diningBudget=diningDollarBudget, dailyDiningBudget=dailyDiningBudget, ldc=LDCCardSwipes, burton=burtonCardSwipes, dining_transactions=dining_transactions, schiller_transactions=schiller_transactions)


def getASI(parseJSON):
    dining_dollars = float(parseJSON["dining_dollars"])
    schillers = float(parseJSON["schillers"])
    swipes = parseJSON["swipes"]

    week = getWeek()
    diningDollars = diningDollarBudget(dining_dollars, week)
    dailyDiningBudget = '$' + str('%.2f' % round(float(diningDollars[1:])/7.00, 2))
    laundryLoadsLeft = laundryLeft(schillers)
    LDCCardSwipes, burtonCardSwipes = LDCBurtonSwipes(swipes)

    return week, diningDollars, dailyDiningBudget, laundryLoadsLeft, LDCCardSwipes, burtonCardSwipes


def diningDollarBudget(dollarsLeft, week):
    return "$" + str('%.2f' % round(dollarsLeft/(10-week), 2))


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
    return week


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
