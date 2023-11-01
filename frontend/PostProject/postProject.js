import { doFetch } from "../helper.js";

const home = document.getElementById('home');
const myPro = document.getElementById('mypro');
const profile = document.getElementById('profile');
const logout = document.getElementById('logout');
const edu = document.getElementById('edu');
const java = document.getElementById('java');
const python = document.getElementById('python');
const js = document.getElementById('js');
const c = document.getElementById('c');
const ml = document.getElementById('ml');
const dl = document.getElementById('dl');
const sd = document.getElementById('sd');
const net = document.getElementById('net');
const data = document.getElementById('data');
const problem = document.getElementById('problem');
const problemInput = document.getElementById('problemInput');
const submit = document.getElementById('submit');
const outcome = document.getElementById('outcome');
const outcomeInput = document.getElementById('outcomeInput');
const deliverable = document.getElementById('deliverable');
const deliverableInput = document.getElementById('deliverableInput');
const editOrCreate = document.getElementById('editOrCreate');
const projName = document.getElementById('projName');
const projStatus = document.getElementById('projStatus');
const projNameInput = document.getElementById('projNameInput');

// Interaction display
function naviDisplay (item) {
    item.addEventListener('mouseover', (event) => {
        item.style.color = `rgb(${0}, ${193}, ${193})`;
    });
    item.addEventListener('mouseleave', (event) => {
        item.style.color = 'white';
    });
};

function inputDisplay (item) {
    item.addEventListener('mouseover', (event) => {
        item.style.borderColor = `rgb(${0}, ${193}, ${193})`;
    });
    item.addEventListener('mouseleave', (event) => {
        item.style.borderColor = `rgba(${128}, ${128}, ${128}, ${0.3})`;
    });
};

function skillDisplay (item) {
    item.addEventListener('mouseover', (event) => {
        item.style.background = `rgba(${0}, ${193}, ${193})`;
    });
    item.addEventListener('mouseleave', (event) => {
        if (item.style.color == 'white') {
            item.style.background = `rgb(${0}, ${193}, ${193})`;
        } else {
            item.style.background = `rgba(${128}, ${128}, ${128}, ${0.3})`;
        }
    });
    item.addEventListener('click', (event) => {
        if (item.style.color == 'black') {
            item.style.color = 'white';
            item.style.background = `rgb(${0}, ${193}, ${193})`;
        } else {
            item.style.color = 'black';
            item.style.background = `rgb(${0}, ${193}, ${193})`;
        };
    });
};

function extraDisplay (item1, item2) {
    item1.addEventListener('mouseover', (event) => {
        item1.style.background = `rgba(${0}, ${193}, ${193}, ${0.5})`;
        item2.style.background = 'white';
    });
    item1.addEventListener('mouseleave', (event) => {
        item1.style.background = 'white';
        item2.style.background = `rgba(${128}, ${128}, ${128}, ${0.1})`;
    });
};

function resumeDisplay (item) {
    item.addEventListener('mouseover', (event) => {
        item.style.background = `rgb(${0}, ${220}, ${220})`;
    });
    item.addEventListener('mouseleave', (event) => {
        item.style.background =  `rgb(${0}, ${193}, ${193})`;
    });
};

naviDisplay(home);
naviDisplay(myPro);
naviDisplay(profile);
naviDisplay(logout);
inputDisplay(projName);
inputDisplay(edu);
skillDisplay(java);
skillDisplay(python);
skillDisplay(js);
skillDisplay(c);
skillDisplay(ml);
skillDisplay(dl);
skillDisplay(sd);
skillDisplay(net);
skillDisplay(data);
extraDisplay(problem, problemInput);
extraDisplay(outcome, outcomeInput);
extraDisplay(deliverable,deliverableInput);
resumeDisplay(submit);

const urlParams = new URLSearchParams(window.location.search);
const edit = urlParams.has('projectId');
const project_id = urlParams.get('projectId');
if (edit) {
    editOrCreate.textContent = 'Edit project';
    doFetch('/profile/project?project_id=' + project_id, "GET").then((data) => {
        console.log(data)
        const projContent =  data[0];
        projNameInput.placeholder = projContent.title;
        console.log(projName)
        projStatus.placeholder = projContent.status;
        problemInput.placeholder = projContent.problem_statement;
        outcomeInput.placeholder = projContent.desired_outcomes;
        deliverableInput.placeholder = projContent.deliverables;
    })
}

submit.addEventListener('click', (event) => {
    
});

logout.addEventListener('click', ()=>{
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('roleId');
    localStorage.removeItem('username');
    localStorage.removeItem('password');
})
