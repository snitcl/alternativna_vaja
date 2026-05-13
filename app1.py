from flask import Flask, render_template, request, redirect, session, jsonify
from tinydb import TinyDB

app = Flask(__name__, template_folder="templates1", static_folder="static1")
app.secret_key = "secret"

# Baza
db = TinyDB('db/notes.json')
users_table = db.table('users')
notes_table = db.table('notes')

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Preverjanje uporabnika brez lambda
        found_user = None
        for u in users_table.all():
            if u['username'] == username:
                found_user = u
                break
        
        if found_user and found_user['password'] == password:
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

        # Preverjanje uporabnika brez lambda
        exists = False
        for u in users_table.all():
            if u['username'] == username:
                exists = True
                break
        
        if not exists:
            users_table.insert({'username': username, 'password': password})
            return redirect("/login")

    return render_template("register.html")


# INDEX
@app.route("/", methods=["GET", "POST"])
def index():
    if "username" not in session:
        return redirect("/login")

    notes = notes_table.all()
    return render_template("index.html", notes=notes)


# AJAX dodajanje zapiska
@app.route("/add_note", methods=["POST"])
def add_note():
    title = request.form["title"]
    content = request.form["content"]
    notes_table.insert({'title': title, 'content': content})
    return jsonify({"title": title, "content": content})


# DELETE
@app.route("/delete/<int:index>")
def delete(index):
    notes = notes_table.all()
    if 0 <= index < len(notes):
        notes_table.remove(doc_ids=[notes[index].doc_id])
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)