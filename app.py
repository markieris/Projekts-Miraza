from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

#Datubāze
def make_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
        
    """)
    conn.commit()
    conn.close()

make_db()

#Start Page
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/page1")
def page1():
    return render_template("page1.html")

#Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

        return redirect("/login")
    
    return render_template("register.html")

#Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            return redirect("/page1")
        else:
            return "Wrong Username or Password!"
        
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
