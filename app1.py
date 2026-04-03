from flask import Flask, render_template, request, redirect, session, jsonify
from tinydb import TinyDB
import os

app = Flask(__name__, template_folder="templates1", static_folder="static1")
app.secret_key = "supersecretkey"  # Za session

# Baza
db_path = os.path.join("db", "notes.json")
db = TinyDB(db_path)
notes_table = db.table("notes")

# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        session["username"] = username
        return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")

# ---------- INDEX ----------
@app.route("/")
def index():
    if "username" not in session:
        return redirect("/login")
    
    notes = notes_table.all()
    # Doc_id dodamo v vsak zapis
    notes_with_id = []
    for note in notes:
        notes_with_id.append({
            "doc_id": note.doc_id,
            "title": note.get("title", ""),
            "content": note.get("content", "")
        })
    
    return render_template("index.html", notes=notes_with_id)

# ---------- ADD NOTE ----------
@app.route("/add", methods=["POST"])
def add_note():
    if "username" not in session:
        return redirect("/login")
    title = request.form["title"]
    content = request.form["content"]
    notes_table.insert({"title": title, "content": content})
    return redirect("/")

# ---------- DELETE NOTE (AJAX) ----------
@app.route("/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    notes_table.remove(doc_ids=[note_id])
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True, port=5000)