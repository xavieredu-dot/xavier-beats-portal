
import os
from datetime import datetime  # to track WHEN they entered
from flask import Flask, render_template, request, redirect, session, url_for
app = Flask(__name__)
app.secret_key = "super_secret_key_123"  # required for sessions

# This finds the "abosolte path" of the project folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "visitors.txt")
COMMENTS_FILE = os.path.join(BASE_DIR, "comments.txt")


@app.route("/")
def index():
    # if they havent logged in, send them to the login page
    if "user" not in session:
        return render_template("login.html")
    return render_template("studio.html", user=session["user"])


@app.route("/login", methods=["POST"])
def logim():
    name = request.form.get("visitor_name")
    session["user"] = name  # Save name in the browser's memory

    # Log the visit with timestamp
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as file:
        file.write(f"{name} entered at {time_now}\n")
    return redirect(url_for('index'))


@app.route("/admin")
def admin_dashboard():
    # 1. ge the visitors
    visitors = []
    try:
        with open("visitors.txt", "r") as f:
            visitors = f.readlines()
    except FileNotFoundError:
        pass

    # 2. get commets
    all_comments = []
    try:
        with open("comments.txt", "r") as f:
            for line in f:
                if "|" in line:
                    parts = line.strip().split("|")
                    all_comments.append({"user": parts[0], "text": parts[1]})
    except FileNotFoundError:
        pass
    return render_template("admin.html", visitors=visitors, comments=all_comments)


@app.route("/")
def idenx():
    if "user" not in session:
        return render_template("login.html")

    all_comments = []
    try:
        with open(COMMENTS_FILE, "r") as file:
            for line in file:
                if "|" in line:
                    parts = line.strip().split("|")
                    all_comments.append({"user": parts[0], "text": parts[1]})
    except FileNotFoundError:
        pass

    return render_template("studio.html", user=session["user"], comments=all_comments)


@app.route("/post_comment", methods=["POST"])
def post_comment():
    user = session.get("user", "Anonymous")
    text = request.form.get("comment_text")

    with open(COMMENTS_FILE, "a") as file:
        file.write(f"{user}|{text}\n")

    return redirect(url_for('index'))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
