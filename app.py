# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request

# create the application object
app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
	return redirect(url_for('home'))
    return render_template('login.html', error = error);

# use decorators to link the function to a url
@app.route('/index.html')
def home():
    return render_template('index.html')  # return a string

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)