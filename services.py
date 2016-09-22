import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ofadmin:ofadmin@localhost/services_p'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import * #User, Category, NewArticle
#from database import db_session

#@app.teardown_appcontext
#def shutdown_session(exception=None):
#    db_session.remove()
#
@app.route('/')
def index():
    return render_template('show_entries.html', entries=None)
    #if 'username' in session:
    #    return 'Logged in as %s' % escape(session['username'])
    #return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/hello/')
def hello(name=None):
    info = os.uname()
    return render_template('hello.html', info=info)

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
            new = NewArticle(request.form['title'],1,request.form['summary'])
            db.session.add(new)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('new.html')

@app.route('/user/<username>')
def show_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('show_user.html', user=user)

"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)
"""

"""
@app.route('/')
def show_entries():
    #db = get_db()
    #cur = db.execute('select title, text from entries order by id desc')
    #entries = cur.fetchall()
    entries = None
    return render_template('show_entries.html', entries=entries)

"""
if __name__ == '__main__':
    app.run()
