from flask import Flask, render_template, request, redirect, session
from tinydb import TinyDB

app = Flask(__name__, template_folder="templates1", static_folder="static1")
app.secret_key = "secret"

# Pot do baze
db = TinyDB('db/notes.json')
users_table = db.table('users')
notes_table = db.table('notes')

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Preverjanje uporabnika
        user = users_table.search(lambda u: u['username'] == username)
        
        if user and user[0]['password'] == password:
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

        
        user = users_table.search(lambda u: u['username'] == username)
        
        if not user:
            users_table.insert({'username': username, 'password': password})
            return redirect("/login")

    return render_template("register.html")


# INDEX
@app.route("/", methods=["GET", "POST"])
def index():
    if "username" not in session:
        return redirect("/login")

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        
        notes_table.insert({'title': title, 'content': content})
        return redirect("/")

    notes = notes_table.all()
    return render_template("index.html", notes=notes)


# DELETE
@app.route("/delete/<int:index>")
def delete(index):
    notes = notes_table.all()

    
    if 0 <= index < len(notes):
        notes_table.remove(doc_ids=[index + 1])

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)