import os

from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQL("sqlite:///database.db")

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def apology(message):

    return render_template("apology.html", message=message)

def login_required(f):
    #Decorate routes to require login.

    #https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/register", methods=["GET", "POST"])
def register():
    # Register user
    if request.method == "POST":

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        username = request.form.get("username")

        if not username:
            return apology("Please enter a username!")

        if len(rows) != 0:
            return apology("Username already exists!")

        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not password:
            return apology("Please enter a password!")

        if not password == confirmation:
            return apology("Passwords do not match!")

        hashed_password = generate_password_hash(password)
        hashed_confirmation = generate_password_hash(confirmation)

        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", username, hashed_password)

        return redirect("/login")

    else:

        return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    # Log user in

    # Forget any previous user_id
    session.clear()

    # Check if user reached route via POST
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Please provide a username!")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Please provide a password!")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("Invalid username and/or password!")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # Check if user reached route via GET 
    else:

        return render_template("login.html")


@app.route("/logout")
def logout():
    # Log user out

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/")
@login_required
def index():
    # index page

    # Queries the database to select all non-blocked contacts of a particular user 
    contacts = db.execute("SELECT * FROM contacts WHERE id = ? AND blocked = 0", session["user_id"])
    
    # returns the index page via GET
    return render_template("index.html", contacts=contacts)


@app.route("/addcontact", methods=["GET", "POST"])
@login_required
def addcontact():
    # Function defined to add a contact to a user's contact database
    if request.method == "POST":
        name = request.form.get("name")
        if not name:
            # if the name field is left absent, returns an apology
            return apology("Please provide a name for the contact!")

        number = request.form.get("number")
        email = request.form.get("email")
        address = request.form.get("address")

        # Inserts the new contact details of a person into the database
        db.execute("INSERT INTO contacts (id, name, number, email, address, blocked) VALUES (?, ?, ?, ?, ?, False)", session["user_id"], name, number, email, address)
        
        # returns the index page once after new contact is added
        return redirect("/")

    else:
        # takes the user to the addcontact html page via GET
        return render_template("addcontact.html")


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    # Function defined to search for a particular contact
    if request.method == "POST":
        name = request.form.get("name")
        if not name:
            # if name field is left blank, returns an apology
            return apology("Please provide a name to be searched!")
        
        # gets all details from the contacts database where the id is the session id of current user and the name searched
        contacts = db.execute("SELECT * FROM contacts WHERE id = ? AND name = ?", session["user_id"], name)

        # takes the user to the searched page showing contacts searched for
        return render_template("searched.html", contacts=contacts)
    else:
        
        # takes the user to search via GET
        return render_template("search.html")



@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    # deletes a particular contact
    if request.method == "POST":
        name = request.form.get("name")
        if not name:
            # if name field is left blank, returns an apology
            return apology("Please enter a name!")
        
        # deletes the contact details from the contacts database of the current user, with name of given contact
        db.execute("DELETE FROM contacts WHERE id = ? and name = ?", session["user_id"], name)


        # returns the user to the index page
        return redirect("/")
    else:
        
        # takes the user to the delete page via GET
        return render_template("delete.html")


@app.route("/block", methods=["GET", "POST"])
@login_required
def block():
    # Function defined to block a particular user
    if request.method == "POST":
        name = request.form.get("name")
        if not name:
            # if the name field is left blank, returns an apology
            return apology("Please enter a name!")


        # updates the contacts database setting the blocked field to 1 (i.e. True) for the current user's given contact name
        db.execute("UPDATE contacts SET blocked = 1 WHERE id = ? AND name = ?", session["user_id"], name)

        #returns the user to the index page
        return redirect("/")

    else: 
        
        # takes the user to the block page via GET
        return render_template("block.html")


@app.route("/blocked")
@login_required
def blocked():
    # Function defined to take the user to the blocked contacts page
    contacts = db.execute("SELECT * FROM contacts WHERE id = ? AND blocked = 1", session["user_id"])
    
    # takes the user to the blocked contacts page
    return render_template("blocked.html", contacts=contacts)

def errorhandler(e):
    # Handle errors
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)