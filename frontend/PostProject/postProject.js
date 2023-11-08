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
let roleId = Number(localStorage.getItem('roleId'));

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
const project_id = Number(urlParams.get('projectId'));

const skillList = ['Java', 'Pthon', 'Javascript', 'C/C++', 'Machine Learning', 'Deep Learning', 'Software Develop', 'Networking', 'Database/Big Data'];

function findSelectedEle(selectedString) {
    console.log(selectedString)
    if (selectedString === 'Java') {
        return java;
    } else if (selectedString === 'Pthon') {
        return python;
    } else if (selectedString === 'Javascript') {
        return js;
    } else if (selectedString === 'C/C++') {
        return c;
    } else if (selectedString === 'Machine Learning') {
        return ml;
    } else if (selectedString === 'Deep Learning') {
        return dl;
    } else if (selectedString === 'Software Develop') {
        return sd;
    } else if (selectedString === 'Networking') {
        return net;
    } else if (selectedString === 'Database/Big Data') {
        return data;
    } 
} 

if (edit) {
    editOrCreate.textContent = 'Edit project';
    doFetch('/profile/project?project_id=' + project_id, "GET").then((data) => {
        console.log(data)
        const projContent =  data[0];
        projNameInput.value = projContent.title;
        console.log(projName)
        let defaultValue = 'Close';
        if (projContent.status === 'is_open') {
            defaultValue = 'Open';
        }
        edu.value = defaultValue;
        problemInput.value = projContent.problem_statement;
        outcomeInput.value = projContent.desired_outcomes;
        deliverableInput.value = projContent.deliverables;
        console.log(skillList)
        console.log(projContent.required_skills)
        if (skillList.includes(projContent.required_skills)) {
            const selectedEle = findSelectedEle(projContent.required_skills);
            console.log(selectedEle)
            selectedEle.classList.add('selected');
        }
    })
}
function selectSkill(selectedSkillElement) {
    document.querySelectorAll('.skill').forEach(skill => {
        skill.classList.remove('selected');
    });

    selectedSkillElement.classList.add('selected');
}

// Add event listeners to each skill
document.querySelectorAll('.skill').forEach(skill => {
    skill.addEventListener('click', function() {
        selectSkill(this);

        
    });
});

submit.addEventListener('click', (event) => { 
    let selectedSkillvalue = document.querySelector('.skill.selected');
    if (selectedSkillvalue !== null) {
        selectedSkillvalue = selectedSkillvalue.textContent;
    } else {
        selectedSkillvalue = '';
    }
    let sta = 'is_open';
    if (edu.value === 'Close') {
        sta = 'closed';
    }
    console.log(typeof outcomeInput.value)
    if (!edit) {
        doFetch('/profile/project', 'POST', {
            "partner_id": roleId,
            "title": projNameInput.value,
            "description": "",
            "problem_statement": problemInput.value,
            "desired_outcomes": outcomeInput.value,
            "required_skills": selectedSkillvalue,
            "deliverables": deliverableInput.value,
            "status": 'is_open'
        })
    } else {
        console.log('hii')
        doFetch('/profile/project', 'PUT', {
            "project_id": project_id,
            "title": projNameInput.value,
            "description": "",
            "problem_statement": problemInput.value,
            "desired_outcomes": outcomeInput.value,
            "required_skills": selectedSkillvalue,
            "deliverables": deliverableInput.value,
            "project_last_updated_at": null,
            "supervisor_id": null,
            "supervisor_being_assigned_at":null,
            "student_id": null,
            "student_being_assigned_at": null,
            "status": 'is_open'
        })
    }
    
    window.location.href = "../BossHome/bossHome.html"
});

logout.addEventListener('click', ()=>{
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('roleId');
    localStorage.removeItem('username');
    localStorage.removeItem('password');
})
