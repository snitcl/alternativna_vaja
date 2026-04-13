from flask import Flask, render_template, request, jsonify, session

# Ustvarimo aplikacijo
app = Flask(__name__, template_folder="templates3", static_folder="static3")
app.secret_key = "12345" 

# Glavna stran
@app.route("/")
def index():
    if "tasks" not in session:
        session["tasks"] = []  
    return render_template("index.html", tasks=session["tasks"])

# Dodajanje opravila (AJAX)
@app.route("/add", methods=["POST"])
def add_task():
    task = request.json.get("task")  
    if "tasks" not in session:
        session["tasks"] = []
    session["tasks"].append(task)    
    return jsonify({"task": task})   

# AJAX
@app.route("/delete", methods=["POST"])
def delete_task():
    task = request.json.get("task")  
    if "tasks" in session and task in session["tasks"]:
        session["tasks"].remove(task)  
    return jsonify({"task": task})    

# Zaženemo aplikacijo
if __name__ == "__main__":
    app.run(debug=True, port=5002)