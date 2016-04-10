"""
Usage: python scrapeScript.py [username] [password]
"""

import sys
import mechanize
import json
import re
import time
import datetime
from bs4 import BeautifulSoup


def main(un, pw):
    br = mechanize.Browser()

    br.set_handle_robots(False)
    br.addheaders = [("User-agent", "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13")]
    sign_in = br.open("https://apps.carleton.edu/login/?dest_page=https%3A%2F%2Fapps.carleton.edu%2Fcampus%2Fonecard%2Fdashboard%2F&msg_uname=onecard_login_blurb&redir_link_text=the%20OneCard%20dashboard")

    br.select_form(nr = 1)

    #un = raw_input("Enter username: ")
    #pw = raw_input("Enter plaintext password, awk: ")

    br["username"] = un
    br["password"] = pw

    logged_in = br.submit()
    logincheck = logged_in.read()

    soup = BeautifulSoup(logincheck, 'html.parser')

    output = {}

    schillers_dining = {}

    for p in soup.find_all('p'):
        p = p.get_text()
        if p.find("Dining") != -1:
            dining = p.split('$')[1]
            schillers_dining['dining_dollars'] = dining
        elif "Schillers-Student" in p:
            schillers = p.split('$')[1]
            schillers_dining['schillers'] = schillers

    output.update(schillers_dining)

    meal_swipes = {}
    for ul in soup.find_all('ul'):
        for li in ul.find_all('li'):
            li = li.get_text()
            if ':' in li:
                meals = li.split(': ')[1]
                if 'Meals remaining today' in li:
                    if len(meal_swipes) < 1:
                        pass
                    else:
                        meal_swipes['meals_today'] = meals
                if 'Meals remaining this week' in li:
                    if len(meal_swipes) < 1:
                        meal_swipes['guest_meals'] = meals
                    else:
                        meal_swipes['meals_week'] = meals
    output.update(meal_swipes)

    table_data = []
    for table in soup.find_all('table', class_="transaction_table"):
        data = {}
        rows = table.find_all('tr')[1:]
        transactions = len(rows)
        date = ''
        for i in range(transactions):
            row = rows[i]
            cols = row.find_all('td')
            row_data = {}
            for col in cols:
                col_type = col['class'][0]
                if col.get_text():
                    row_data[col_type] = col.get_text()
                elif col_type == 'date':
                    row_data[col_type] = date
            date = row_data['date']
            day = getDay(date)
            row_data['day'] = day
            data[i] = row_data
        table_data.append(data)
    output['spending'] = table_data[0]
    output['swipes'] = table_data[1]

    transactions = []
    for k,v in output['spending'].items():
        transactions.append((k,v))
    transactions.sort(key=lambda tup: tup[0], reverse=True)
    dd_balance = float(output['dining_dollars'])
    s_balance = float(output['schillers'])
    dining_transactions = '['
    schiller_transactions = '['
    for t in transactions:
        #print t[1].items()
        comment = t[1].items()[0][1]
        amount = float(t[1].items()[1][1][2:])
        day = t[1].items()[5][1]
        if comment == 'Dining Dollars':
            dining_transactions += '{day: %s, balance: %s,}, ' % (day, dd_balance)
            dd_balance = dd_balance + amount
        if comment == 'Schillers-Student':
            schiller_transactions += '{day: %s, balance: %s,}, ' % (day, s_balance)
            s_balance = s_balance + amount
    dining_transactions = dining_transactions[:-2] + ']'
    schiller_transactions = schiller_transactions[:-2] + ']'
    if len(dining_transactions) < 2:
        dining_transactions = '[{day: 0, balance: %s,}, {day: %s, balance: %s,}]' % (dd_balance, getDay(time.strftime('%a, %b %d %Y')), dd_balance)
    if len(schiller_transactions) < 2:
        schiller_transactions = '[{day: 0, balance: %s,}, {day: %s, balance: %s,}]' % (s_balance, getDay(time.strftime('%a, %b %d %Y')), s_balance)

    outputJSON = json.dumps(output)
    return outputJSON, dining_transactions, schiller_transactions


def getDay(date_string):
    end_of_term = datetime.date(2016, 6, 7)
    nice_date = datetime.datetime.strptime(date_string, '%a, %b %d %Y').date()
    delta = end_of_term - nice_date
    day = delta.days
    return 72 - day

if __name__ == '__main__':
    un = sys.argv[1]
    pw = sys.argv[2]
    outputJSON = main(un, pw)
