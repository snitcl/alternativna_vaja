from flask import Flask, render_template, request, session
from tinydb import TinyDB

app = Flask(
    __name__,
    template_folder="templates3",
    static_folder="static3"
)

app.secret_key = "123"

db = TinyDB("db/polls.json")
polls = db.table("polls")
# izbira barv
if len(polls) == 0:
    polls.insert({
        "question": "Katera je tvoja najljubša barva?",
        "options": ["Rdeča", "Modra", "Zelena", "Rumena"],
        "votes": [0, 0, 0, 0]
    })

# index
@app.route("/")
def index():
    poll = polls.all()[0]
    if "voted" not in session:
        session["voted"] = False
    return render_template(
        "index.html",
        poll=poll,
        voted=session["voted"]
    )

# glasovanje
@app.route("/vote", methods=["POST"])
def vote():
    poll = polls.all()[0]
    if session["voted"] == False:
        option = int(request.form["option"])
        poll["votes"][option] = poll["votes"][option] + 1
        polls.update(
            {"votes": poll["votes"]},
            doc_ids=[polls.all()[0].doc_id]
        )
        session["voted"] = True
    return "glas oddan"

# resetirj - AJAX
@app.route("/reset")
def reset():
    poll = polls.all()[0]
    poll["votes"] = [0, 0, 0, 0]
    polls.update(
        {"votes": poll["votes"]},
        doc_ids=[polls.all()[0].doc_id]
    )
    session["voted"] = False
    return "reset"

if __name__ == "__main__":
    app.run(debug=True, port=5002)