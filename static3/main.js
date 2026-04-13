function addTask() {
    let taskInput = document.getElementById("newTask");
    let task = taskInput.value;
    if (task === "") {
        alert("Vpiši opravilo!");
        return;
    }

    fetch("/add", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({task: task})
    })
    .then(response => response.json())
    .then(data => {
        let ul = document.getElementById("taskList");
        let li = document.createElement("li");
        li.innerHTML = data.task + ' <button onclick="deleteTask(\'' + data.task + '\')">Izbriši</button>';
        ul.appendChild(li);
        taskInput.value = "";
    });
}

function deleteTask(task) {
    fetch("/delete", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({task: task})
    })
    .then(response => response.json())
    .then(data => {
        let ul = document.getElementById("taskList");
        ul.innerHTML = "";
        fetch("/")
        .then(resp => resp.text())
        .then(html => {
            let parser = new DOMParser();
            let doc = parser.parseFromString(html, "text/html");
            let newList = doc.getElementById("taskList");
            ul.innerHTML = newList.innerHTML;
        });
    });
}