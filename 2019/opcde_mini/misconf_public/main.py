import sys

from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for

app = Flask(__name__)
app.debug = False
app.secret_key = 'wkadkswkrhcnfrmsgkslsjanvlrhsgkek1234'


@app.route("/")
def index():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        if session['role'] == 'guest':
            message = open('./static/message').read()
        elif session['role'] == 'admin':
            message = open('/flag').read()

        return render_template('login.html', message=message)

@app.route("/login", methods=['POST'])
def login():
    if request.method != 'POST':
        return redirect(url_for('index'))

    username = request.form.get('username')
    password = request.form.get('password')

    if username and password:
        session['logged_in'] = True
        session['username'] = username
        session['password'] = password
        session['role'] = 'admin'

    return redirect(url_for('index'))


@app.route("/logout")
def logout():
    if session.get('logged_in'):
        for key in list(session.keys()):
            session.pop(key)

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
