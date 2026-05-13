"""from flask import Flask, render_template, request, redirect, session, jsonify
import os
from tinydb import TinyDB

app = Flask(__name__, template_folder="templates2", static_folder="static2")
app.secret_key = "supersecretkey"

users = []
posts = []

db2 = TinyDB('db2/app2.json')
users_table = db2.table('users')
posts_table = db2.table('posts')

UPLOAD_FOLDER = os.path.join("static2", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        for user in users:
            if user["username"] == username and user["password"] == password:
                session["username"] = username
                return redirect("/")
    return render_template("login.html")

# LOGOUT
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")

# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username and all(user["username"] != username for user in users):
            users.append({"username": username, "password": password})
            return redirect("/login")
    return render_template("register.html")

# INDEX
@app.route("/", methods=["GET", "POST"])
def index():
    if "username" not in session:
        return redirect("/login")
    
    if request.method == "POST":
        content = request.form["content"]
        filename = None
        file = request.files.get("image")
        if file and file.filename != "":
            filename = file.filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
        posts.append({"username": session["username"], "content": content, "image": filename})
        return redirect("/")
    
    return render_template("index.html", posts=posts, username=session["username"])

# DELETE - AJAX
@app.route("/delete/<int:index>", methods=["POST"])
def delete(index):
    if 0 <= index < len(posts):
        if posts[index]["username"] == session.get("username"):
            # izbrišemo tudi sliko
            if posts[index]["image"]:
                try:
                    os.remove(os.path.join(UPLOAD_FOLDER, posts[index]["image"]))
                except:
                    pass
            posts.pop(index)
            return jsonify({"success": True})
    return jsonify({"success": False})

if __name__ == "__main__":
    app.run(debug=True, port=5001)"""

from flask import Flask, render_template, request, redirect, session, jsonify
from tinydb import TinyDB
import os

# ====== Flask aplikacija ======
app = Flask(__name__, template_folder="templates2", static_folder="static2")
app.secret_key = "supersecretkey"

# ====== BAZA ======
# Datoteka db2/app2.json bo vsebovala uporabnike in objave
db2 = TinyDB('db2/app2.json')
users_table = db2.table('users')
posts_table = db2.table('posts')

# ====== FOLDER ZA SLIKE ======
UPLOAD_FOLDER = "static2/uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ====== LOGIN ======
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Preprosto preverjanje uporabnika v bazi
        user_found = None
        for u in users_table.all():
            if u['username'] == username and u['password'] == password:
                user_found = u
                break

        if user_found:
            session["username"] = username
            return redirect("/")

    return render_template("login.html")

# ====== LOGOUT ======
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")

# ====== REGISTER ======
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Preverimo, ali uporabnik že obstaja
        exists = False
        for u in users_table.all():
            if u['username'] == username:
                exists = True
                break

        if not exists:
            users_table.insert({'username': username, 'password': password})
            return redirect("/login")

    return render_template("register.html")

# ====== INDEX / OBJAVE ======
@app.route("/", methods=["GET", "POST"])
def index():
    if "username" not in session:
        return redirect("/login")
    
    if request.method == "POST":
        content = request.form["content"]
        file = request.files.get("image")
        filename = None
        if file and file.filename != "":
            filename = file.filename
            # Shranimo sliko v folder static2/uploads
            file.save(os.path.join(UPLOAD_FOLDER, filename))
        # Dodamo objavo v bazo
        posts_table.insert({
            'username': session['username'],
            'content': content,
            'image': filename
        })
        return redirect("/")

    # Pridobimo vse objave iz baze
    posts = posts_table.all()
    return render_template("index.html", posts=posts, username=session["username"])

# ====== DELETE – AJAX ======
@app.route("/delete/<int:index>", methods=["POST"])
def delete(index):
    posts = posts_table.all()
    if 0 <= index < len(posts):
        if posts[index]['username'] == session.get('username'):
            # izbrišemo sliko, če obstaja
            if posts[index]['image']:
                try:
                    os.remove(os.path.join(UPLOAD_FOLDER, posts[index]['image']))
                except:
                    pass
            # odstranimo objavo iz baze
            posts_table.remove(doc_ids=[posts[index].doc_id])
            return jsonify({"success": True})
    return jsonify({"success": False})

# ====== ZAGON APLIKACIJE ======
if __name__ == "__main__":
    app.run(debug=True, port=5001)