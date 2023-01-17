import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    data = 0
    cash = 0
    # fetch owned stocks symbols and amounts
    stocks = db.execute("SELECT symbol, amount FROM holdings WHERE user_id=?", session["user_id"])

    # fetch current price of each stock
    prices = []
    names = []
    for entry in stocks:
        prices.append(lookup(entry['symbol'])["price"])
        names.append(lookup(entry['symbol'])["name"])

    # fetch users cash balance
    cash = db.execute("SELECT cash from users where id=?", session["user_id"])[0]["cash"]

    # calculate users total balance (stocks value plus cash)
    grand_total = 0
    count = 0
    totals = []
    for entry in stocks:
        grand_total = grand_total + entry["amount"] * prices[count]
        # save totals
        totals.append(usd(entry["amount"] * prices[count]))
        count = count + 1
    grand_total = grand_total + cash

    # convert floats to formatted strings
    grand_total = usd(grand_total)
    cash = usd(cash)
    count = 0
    for price in prices:
        prices[count] = usd(price)
        count = count + 1

    # zip and send data
    data = zip(stocks, prices, names, totals)
    return render_template("index.html", data=data, cash=cash, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # handle post request
    if request.method == "POST":

        # Ensure user entered a symbol
        if not request.form.get("symbol"):
            return apology("enter a symbol")

        # Ensure user entered an amount of shared
        elif not request.form.get("shares"):
            return apology("enter an amount")

        # Ensure shares amount is an integer
        elif not request.form.get("shares").isdigit():
            return apology("amount must be integer", 400)

        # Ensure symbol is valid
        data = lookup(request.form.get("symbol"))
        if data == None:
            return apology("Symbol does not exist")

        # Ensure amount of shares is > 0
        elif int(request.form.get("shares")) <= 0:
            return apology("amount too little")

        # Ensure user can afford shares
        redirect("/buy")
        amount = float(request.form.get("shares"))
        price = float(data["price"])
        budget = float(db.execute("SELECT cash from users WHERE id=? LIMIT 1", session["user_id"])[0]["cash"])
        if price * amount > budget:
            return apology("You cannot afford this")

        # Make purchase and keep track of it
        else:
            now = datetime.datetime.now()
            # Add transaction to history table
            db.execute("INSERT INTO transactions (user_id, symbol, amount, price, time, type) VALUES (?, ?, ?, ?, ?, 'buy')",
                       session["user_id"], request.form.get("symbol"), request.form.get("shares"), price, now)

            # check if this share is already a holding
            share_count = db.execute("SELECT COUNT (amount) FROM holdings WHERE user_id=? AND symbol=?",
                                     session["user_id"], request.form.get("symbol"))[0]["COUNT (amount)"]
            if share_count == 0:
                # Add bought shares to users holdings table
                db.execute("INSERT INTO holdings (user_id, symbol, amount) VALUES (?, ?, ?)",
                           session["user_id"], request.form.get("symbol"), amount)
            else:
                # calculate new total amount users has of this share
                amount_old = float(db.execute("SELECT amount FROM holdings WHERE user_id=? AND symbol=?",
                                              session["user_id"], request.form.get("symbol"))[0]["amount"])
                amount_updated = amount_old + amount
                # Update amount of shares
                db.execute("UPDATE holdings SET amount=? WHERE user_id=? AND symbol=?",
                           amount_updated, session["user_id"], request.form.get("symbol"))

            # reduce users cash accordingly
            balance = budget - price * amount
            db.execute("UPDATE users SET cash = ? WHERE id=?", balance, session["user_id"])
            flash("Transaction complete!")

            # Return user to homepage
            return redirect("/")

    # handle GET request
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # fetch data
    data = db.execute("SELECT type, symbol, price, amount, time FROM transactions WHERE user_id=?", session["user_id"])

    # format floats with dollar signs
    for dict in data:
        for key in dict:
            if key == "price":
                dict[key] = usd(dict[key])

    return render_template("history.html", data=data)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and any random password is entered. should be: password is correct
        if len(rows) != 1:
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/changepw", methods=["GET", "POST"])
@login_required
def changepw():
    """ Change user password"""
    # Handle POST request
    if request.method == "POST":

        # Ensure user has entered password
        if not request.form.get("password"):
            return apology("must enter password", 400)

        # Ensure user has entered new password
        elif not request.form.get("newpw"):
            return apology("must enter new password", 400)

        # Ensure user has confirmed new password
        elif not request.form.get("confirmation"):
            return apology("must confirm new password", 400)

        # Ensure old password is correct
        rows = db.execute("SELECT * FROM users WHERE id=?", session["user_id"])
        if not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("old password wrong", 400)

        # Ensure password matches confirmation
        elif request.form.get("newpw") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # Change password in db
        else:
            db.execute("UPDATE users SET hash=? WHERE id=?", generate_password_hash(
                request.form.get("confirmation")), session["user_id"])
            flash("Changed password!")
            return redirect("/")

    # Handle GET request
    else:
        return render_template("changepw.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("must provide symbol")
        else:
            symbol = request.form.get("symbol")
            data = lookup(symbol)
            if data == None:
                return apology("Symbol does not exist")
            else:
                name = data["name"]
                price = usd(data["price"])
                smb = data["symbol"]
                redirect("/quote")
                return render_template("quoted.html", name=name, price=price, smb=smb)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure a username was entered
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was entered
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password is confirmed by user
        elif not request.form.get("confirmation"):
            return apology("please confirm password", 400)

        # Ensure password matches confirmation
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        redirect("/register")
        username = request.form.get("username")
        users_same_name = db.execute("SELECT username FROM users WHERE username=?", username)

        # Check if username already taken
        if not len(users_same_name) == 0:
            return apology("username already in use", 400)

        # Enter new user into table
        pw = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, pw)

        flash("You are now registered!")
        return render_template("login.html")

    # User reached with GET
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # fetch all of users stocks
    stocks = db.execute("SELECT symbol FROM holdings WHERE user_id=?", session["user_id"])

    # Handle POST requests
    if request.method == "POST":

        # ensure user enters amount of shares to sell
        if not request.form.get("shares"):
            return apology("must enter amount to sell", 400)

        # ensure amount is integer
        if not request.form.get("shares").isdigit():
            return apology("amount must be integer", 400)

        # ensure user select stock to sell
        elif not request.form.get("symbol"):
            return apology("must select stock to sell", 400)

        # ensure user still has holdings in the selected stock
        # elif stocks[request.form.get("symbol")] == None:
            # return apology("you do not own this share", 403)

        # ensure number of shares to sell does not exceed number of owned shares
        amount_old = db.execute("SELECT amount FROM holdings WHERE user_id=? AND symbol=?",
                                session["user_id"], request.form.get("symbol"))[0]["amount"]
        if int(request.form.get("shares")) > amount_old:
            return apology("cannot sell more than owned", 400)

        # conduct sale
        else:
            now = datetime.datetime.now()
            data = lookup(request.form.get("symbol"))
            price = float(data["price"])
            amount = float(request.form.get("shares"))

            # Add transaction to history table
            db.execute("INSERT INTO transactions (user_id, symbol, amount, price, time, type) VALUES (?, ?, ?, ?, ?, 'sell')",
                       session["user_id"], request.form.get("symbol"), request.form.get("shares"), price, now)

            # Calculate new total amount of shares user has
            amount_old = float(db.execute("SELECT amount FROM holdings WHERE user_id=? AND symbol=?",
                               session["user_id"], request.form.get("symbol"))[0]["amount"])
            amount_updated = amount_old - amount

            # Update amount of shares
            if amount_updated == 0:
                db.execute("DELETE FROM holdings WHERE symbol=? AND user_id=?", request.form.get("symbol"), session["user_id"])
            else:
                db.execute("UPDATE holdings SET amount=? WHERE user_id=? AND symbol=?",
                           amount_updated, session["user_id"], request.form.get("symbol"))

            # Add cash in users table
            old_cash = float(db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"])
            new_cash = old_cash + price * amount
            db.execute("UPDATE users SET cash=? WHERE id=?", new_cash, session["user_id"])

            # Send data and message
            flash("Sale completed successfully!")
            redirect("/sell")
            return redirect("/")

    # Handle GET requests
    else:
        return render_template("sell.html", stocks=stocks)
