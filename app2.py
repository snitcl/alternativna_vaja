from flask import Flask, render_template, request, redirect, session, jsonify
import os

app = Flask(__name__, template_folder="templates2", static_folder="static2")
app.secret_key = "supersecretkey"

users = []
posts = []

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
    app.run(debug=True, port=5001)