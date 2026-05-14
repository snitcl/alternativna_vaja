from flask import Flask, render_template, request, redirect, session, jsonify
from tinydb import TinyDB
import os


app = Flask(__name__, template_folder="templates2", static_folder="static2")
app.secret_key = "lala"

# baza
db2 = TinyDB('db2/app2.json')
users_table = db2.table('users')
posts_table = db2.table('posts')

# shrani slike
UPLOAD_FOLDER = "static2/uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# prijava
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_found = None
        for u in users_table.all():
            if u['username'] == username and u['password'] == password:
                user_found = u
                break

        if user_found:
            session["username"] = username
            return redirect("/")

    return render_template("login.html")

# odjava
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")

# registriraj
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # preveri uporabnika
        exists = False
        for u in users_table.all():
            if u['username'] == username:
                exists = True
                break
        # ce ne obtsaja
        if not exists:
            users_table.insert({'username': username, 'password': password})
        return redirect("/login")

    return render_template("register.html")
# index
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
            # shrani sliko
            file.save(os.path.join(UPLOAD_FOLDER, filename))
        # doda v bazo
        posts_table.insert({
            'username': session['username'],
            'content': content,
            'image': filename
        })
        return redirect("/")

    posts = posts_table.all()
    return render_template("index.html", posts=posts, username=session["username"])

# izbrisi - AJAX
@app.route("/delete/<int:index>", methods=["POST"])
def delete(index):
    posts = posts_table.all()
    if 0 <= index < len(posts):
        if posts[index]['username'] == session.get('username'):
            if posts[index]['image']:
                try:
                    os.remove(os.path.join(UPLOAD_FOLDER, posts[index]['image']))
                except:
                    pass
            # izbirisi objavo
            posts_table.remove(doc_ids=[posts[index].doc_id])
            return jsonify({"success": True})
    return jsonify({"success": False})

if __name__ == "__main__":
    app.run(debug=True, port=5001)