from flask import Flask, render_template, request, redirect, session
from tinydb import TinyDB

app = Flask(__name__, template_folder="templates3", static_folder="static3")
app.secret_key = "secret"

db = TinyDB("db/polls.json")
polls = db.table("polls")

if len(polls) == 0:
    polls.insert({
        "question": "Katera je tvoja najljubša barva?",
        "options": ["Rdeča", "Modra", "Zelena", "Rumena"],
        "votes": [0, 0, 0, 0]
    })

@app.route("/", methods=["GET", "POST"])
def index():
    poll = polls.all()[0]  

    
    if "has_voted" not in session:
        session["has_voted"] = False

    
    if request.method == "POST":
        if session["has_voted"] == False:
            izbrana = int(request.form["option"])  
            poll["votes"][izbrana] = poll["votes"][izbrana] + 1  
            polls.update({"votes": poll["votes"]}, doc_ids=[polls.all()[0].doc_id])
            session["has_voted"] = True
        return redirect("/")

    
    return render_template("index.html", poll=poll, has_voted=session["has_voted"])


@app.route("/reset")
def reset():
    poll = polls.all()[0]
    poll["votes"] = [0,0,0,0]
    polls.update({"votes": poll["votes"]}, doc_ids=[polls.all()[0].doc_id])
    session["has_voted"] = False
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=5002)