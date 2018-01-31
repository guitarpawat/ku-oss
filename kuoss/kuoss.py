import os
import bcrypt
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# Create the application instance
app = Flask(__name__)
# Load config from this file
app.config.from_object(__name__)
# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'data.db'),
    SECRET_KEY='NotForProduction',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# TEAR DOWN BELOW
@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# APP ROUTE BELOW
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'TODO!'
    return render_template('login.html')

# COMMAND LINE INTERFACE BELOW
def init_db():
    db = get_db()
    with app.open_resource('init.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.cli.command('newuser')
def new_user():
    user = input("Please Enter Username: ")
    pass1 = str.encode(input("Please Enter Password: "))
    hashed = bcrypt.hashpw(pass1, bcrypt.gensalt())
    pass2 = str.encode(input("Please Enter Password Again: "))
    if not bcrypt.checkpw(pass2, hashed):
        print("Password Mismatched")
        return 1
    uid = input("Please Enter Your ID: ")
    name = input("Please Enter Your Name: ")
    sname = input("Please Enter Your Surname: ")
    stat = int(input("Please Enter Your Status: "))
    data = [uid,user,hashed,name,sname,stat]
    db = get_db()
    db.execute('INSERT INTO users (uid,user,hash,name,surname,status) VALUES (?,?,?,?,?,?)', data)
    db.commit()
    print("User Added Successful")