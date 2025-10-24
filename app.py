from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3, os
app = Flask(__name__)
app.secret_key = "supersecret"


# --- Create Database ---
def init_db():
    db_path = app.config.get("DATABASE", "database.db") 
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                message TEXT
            )
        """)
        conn.commit()
        conn.close()
init_db()

@app.route("/", methods=["GET", "POST"])
def home():
    db_path = app.config.get("DATABASE", "database.db")
    if request.method == "POST":
        name = request.form["name"]
        message = request.form["message"]
        # Save name in session (temporary storage)
        session["username"] = name
        # Save data in database
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("INSERT INTO submissions (name, message) VALUES (?, ?)", (name, message))
        conn.commit()
        conn.close()
        return redirect(url_for("thank_you"))
    return render_template("form.html")

@app.route("/thank-you")
def thank_you():
    username = session.get("username", "Guest")
    return f"Thank you, {username}! Your form has been submitted."


@app.route("/chin")
def chin():
    return f"Submit Your Message"

if __name__ == "__main__":
    app.run(debug=True)