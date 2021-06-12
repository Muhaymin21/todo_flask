const inputBox = document.querySelector(".inputField input");
const todoList = document.querySelector("#todosContainer .todoList");
const lists = document.querySelector(".todoList");
const errSpan = document.querySelector("#errorspan");

window.addEventListener('DOMContentLoaded', () => {
    document.querySelector("#newTodoItem").addEventListener('click', addNewLiItem);
    document.querySelector('#addNewList').addEventListener('click', addNewList);
});

inputBox.onkeyup = () => {
    let inputFilter = inputBox.value.toUpperCase();
    const liItems = todoList.getElementsByTagName("li");
    for (let i = 0; i < liItems.length; i++) {
        let liItem = liItems[i];
        if (liItem) {
            let txtValue = liItem.textContent || liItem.innerText;
            if (txtValue.toUpperCase().indexOf(inputFilter) > -1) {
                liItem.style.display = "";
            } else {
                liItem.style.display = "none";
            }
        }
    }
};

function addNewList() {
    let userEnteredValue = prompt('What list you want to add?').trim();
    if (userEnteredValue) {
        toggleLoader();
        fetch('/todos/list/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "data": userEnteredValue
            }),
        }).then(response => response.json()).then(
            data => {
                let newLiTag = document.createElement('li');
                newLiTag.id = "list_" + data.id;
                newLiTag.innerHTML = `<a href="/list/${data.id}">${userEnteredValue}</a>
                        <span class="icon" onclick="deleteTask(${data.id}, 'list')"><i class="fas fa-trash"></i></span>`;
                lists.appendChild(newLiTag);
                inputBox.value = "";
                errSpan.innerHTML = "";
            }
        ).catch(err => {
            console.error(err);
            errSpan.innerHTML = "Unknown error.";
        }).finally(toggleLoader);
    }
}


function addNewLiItem() {
    let userEnteredValue = prompt('What todo you want to add?').trim();
    if (userEnteredValue) {
        toggleLoader();
        fetch('/todos/todo/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "data": userEnteredValue,
                "list_id": todoList.id
            }),
        }).then(response => response.json()).then(
            data => {
                let newLiTag = document.createElement('li');
                newLiTag.id = "todo_" + data.id;
                newLiTag.innerHTML = `<label for="checkbox_${data.id}">
            <input onclick="checkUpdate(this)" id="checkbox_${data.id}" data-id="${data.id}" type="checkbox"/>
            ${userEnteredValue}
            <span class="icon" onclick="deleteTask(${data.id}, 'todo')">
            <i class="fas fa-trash"></i>
            </span></label>`;
                const pendingTasksNumb = document.querySelector(".pendingTasks");
                pendingTasksNumb.textContent = (parseInt(pendingTasksNumb.textContent) + 1).toString();
                todoList.appendChild(newLiTag);
                inputBox.value = "";
                errSpan.innerHTML = "";
            }
        ).catch(err => {
            console.error(err);
            errSpan.innerHTML = "Unknown error."
        }).finally(toggleLoader);
    }
}


function deleteTask(index, whattodelete) {
    toggleLoader();
    fetch('/todos/' + whattodelete + '/delete', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            "id": index
        }),
    }).then(response => response.json()).then(data => {
        if (data.success) {
            if (whattodelete === 'todo') {
                todoList.removeChild(document.querySelector("#todo_" + index));
                const pendingTasksNumb = document.querySelector(".pendingTasks");
                pendingTasksNumb.textContent = (parseInt(pendingTasksNumb.textContent) - 1).toString();
                errSpan.innerHTML = "";
            } else
                lists.removeChild(document.querySelector("#list_" + index));
        } else errSpan.innerHTML = "Unknown error.";
    }).catch(err => {
        console.error(err);
        errSpan.innerHTML = "Unknown error.";
    }).finally(toggleLoader);
}

let loaderStatus = false;

function toggleLoader() {
    const modal = document.querySelector('.modal');
    let display;
    if (loaderStatus)
        display = "none";
    else
        display = "flex";
    modal.style.display = display;
    loaderStatus = !loaderStatus;
}

function checkUpdate(e) {
    const newState = e.checked;
    const pendingTasksNumb = document.querySelector(".pendingTasks");
    let newValue;
    console.log();
    if (newState)
        newValue = -1;
    else
        newValue = 1;
    pendingTasksNumb.textContent = (parseInt(pendingTasksNumb.textContent) + newValue).toString();
    fetch('/todos/update', {
        method: 'put',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "id": e.dataset.id,
            "completed": newState
        }),
    }).then(response => response.json()).then(response => {
        if (response.success)
            errSpan.innerHTML = "";
        else
            errSpan.innerHTML = "Unknown error.";
    }).catch(err => {
        console.log(err);
        errSpan.innerHTML = "Unknown error.";
    });
}