import { doFetch } from "../helper.js";

const home = document.getElementById('home');
const myPro = document.getElementById('mypro');
const profile = document.getElementById('profile');
const logout = document.getElementById('logout');
const detail = document.getElementById('detail');
const add = document.getElementById('add');
const container = document.getElementById('container');
const edit = document.getElementById('edit');
const upload = document.getElementById('upload');
const view = document.getElementById('view');
const score = document.getElementById('score');
const spObj = document.getElementById('spObj');
const deadline = document.getElementById('deadline');
const userStory = document.getElementById('userStory');
const stReport = document.getElementById('stReport');
const suFeedback = document.getElementById('suFeedback');
const status = document.getElementById('status');
const proName = document.getElementById('proName');
const roleId = Number(localStorage.getItem('roleId')); 
const role = localStorage.getItem('role');
const urlParams = new URLSearchParams(window.location.search);
const project_id = Number(urlParams.get('projectId')); 

// Interaction color display
function naviDisplay (item) {
    item.addEventListener('mouseover', (event) => {
        item.style.color = `rgb(${0}, ${193}, ${193})`;
    });
    item.addEventListener('mouseleave', (event) => {
        item.style.color = 'white';
    });
};

function buttonDisplay (item) {
    item.addEventListener('mouseover', (event) => {
        item.style.background = `rgb(${0}, ${230}, ${230})`;
    });
    item.addEventListener('mouseleave', (event) => {
        item.style.background = `rgb(${0}, ${193}, ${193})`;
    });
};

function sprintDisplay (item) {
    item.addEventListener('mouseover', (event) => {
        item.style.borderColor = `rgb(${0}, ${193}, ${193})`;
    });
    item.addEventListener('mouseleave', (event) => {
        item.style.borderColor = `rgba(${0}, ${0}, ${0}, ${0})`;
    });
};

add.addEventListener('mouseover', (event) => {
    add.style.color = `rgb(${0}, ${220}, ${220})`;
});
add.addEventListener('mouseleave', (event) => {
    add.style.color = `rgb(${0}, ${160}, ${160})`;
});

// interaction dynamic display
naviDisplay(home);
naviDisplay(myPro);
naviDisplay(profile);
naviDisplay(logout);
buttonDisplay(detail);
buttonDisplay(edit);
buttonDisplay(view);
buttonDisplay(upload);

function loadSprints (num, clickSp1, clickLastSprint) {
    container.textContent = '';
    for (let i = 1; i <= num; i++) {
        const sprint = document.createElement('input');
        sprint.type = 'button'
        sprint.className = 'sprint';
        sprint.value = 'Sprint ' + i;
        if (num == 1) {
            sprint.style.color = 'white';
            sprint.style.background = `rgb(${0}, ${193}, ${193})`;
        };
        container.appendChild(sprint);
        sprintDisplay(sprint);
        clickSprint(sprint);
        if ((clickLastSprint && i === num) || (clickSp1 && i === 1)) {
            sprint.click();
        }
    };
};
function getSprintNumber(sprintstring) {
    return Number(sprintstring[sprintstring.length - 1]);
}
function clickSprint (item) {
    console.log(item)
    item.addEventListener('click', (event) => {
        for (let i = 0; i < container.children.length; i++) {
            const child = container.children[i];
            child.classList.remove('selectedSprint');
            child.style.background = 'white';
            child.style.color = `rgb(${0}, ${193}, ${193})`;
        };
        item.style.background = `rgb(${0}, ${193}, ${193})`;
        item.style.color = 'white';
        item.classList.add("selectedSprint");
        showProgressContent(project_id, getSprintNumber(item.value));
    });
};
function getSelectedSprintEle() {
    return document.querySelector('.selectedSprint');
}

detail.addEventListener("click", ()=>{
    if (role === 'partner') {
        window.location.href = "../BossProject/BProjectInfo.html" + '?id=' + project_id;
    } else {
        window.location.href = '../ProjectInfo/projectInfo.html' + '?id=' + project_id;
    }
})
if (role === 'partner') {
    upload.classList.add('hide');
    edit.value = 'End sprint and give mark'
    edit.style.width = '230px';
}
let editState = false;
if(edit.value === 'Submit') {
    editState = true;
}
function fisrLettertoUpper(string){
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function changeStatusColor(statusStr) {
    if (statusStr === 'done') {
        status.style.backgroundColor = '#008001';
    } else if (statusStr === 'in progress') {
        status.style.backgroundColor = '#0003ff';
    } else {
        status.style.backgroundColor = '#efe202';
    }
}

function showProgressContent(project_id, nSprint) {
    doFetch('/progress/all_progress/' + project_id, 'GET').then( data =>{
        if (nSprint <= data.all_progress.length) {
            console.log(nSprint)
            const currProgress = data.all_progress[nSprint - 1];
            console.log(currProgress);
            spObj.value = currProgress.sprint_objective;
            userStory.value = currProgress.user_story;
            stReport.value = currProgress.content;
            suFeedback.value = currProgress.partner_feedback;
            status.textContent = fisrLettertoUpper(currProgress.status);
            changeStatusColor(currProgress.status)
            console.log('hiii');
            console.log(score.value)
            score.value = currProgress.partner_mark ? currProgress.partner_mark.toString():'Sprint not finished, mark will be given when finished';
           
        }
    })

}


add.addEventListener('click', (event) => {
    doFetch('/profile/project?project_id=' + project_id, "GET").then(data =>{
        const student_id = data[0].student_id;
        doFetch('/progress', 'POST', {
            "project_id": project_id,
            "student_id": student_id,
            "content": "",
            "sprint_objective": "",
            "user_story": "",
            "status": "to do"
        }).then(data => {
            doFetch('/progress/all_progress/' + project_id, 'GET').then(data =>{
                const progressList = data.all_progress;
                loadSprints(progressList.length, false, true);
            })
        })
    })
});

doFetch('/progress/all_progress/' + project_id, 'GET').then(data =>{
    const progressList = data.all_progress;
    if (progressList.length === 0) {
        add.click();
    }
    proName.textContent = data.project.title;
    loadSprints(progressList.length, true, false);
})


edit.addEventListener('click', () => {
    console.log(getSelectedSprintEle())

    let spNum = getSprintNumber(getSelectedSprintEle().value) - 1;
    if (!editState) {
        edit.value = 'Submit';
        if (role === 'partner') {
            score.disabled = false;
        }
        if (role === 'student') {
            spObj.disabled = false;
            deadline.disabled = false;
            userStory.disabled = false;
            stReport.disabled = false;
        }
    
        if (role === 'supervisor') {
            suFeedback.disabled = false;
        }
        editState = true;
    } else {
        if (role === 'partner') {
            edit.value = 'End sprint and give mark';
        } else {
            edit.value = 'Edit';
        }
        score.disabled = true;
        spObj.disabled = true;
        deadline.disabled = true;
        userStory.disabled = true;
        stReport.disabled = true;
        suFeedback.disabled = true;
        editState = false;
        doFetch(`/progress/${project_id}/${spNum}`, 'GET').then(pInfo => {
            const progressId = pInfo.project_progress_id;

            console.log(Number(score.value))
            doFetch("/progress/partner_feedback/" + progressId, "PUT", {
                "partner_id": pInfo.partner_id,
                "partner_feedback": suFeedback.value,
                "partner_mark": Number(score.value)
            }).then(data => {
                let statusStr = 'to do';
                console.log(data)
                if (data.partner_mark !== null && data.partner_mark !== 11) {
                    statusStr = "done";
                } else if (stReport.value !== "") {
                    statusStr = "in progress";
                }
                status.textContent = fisrLettertoUpper(statusStr);
                changeStatusColor(statusStr);
                doFetch("/progress/text/" + progressId, "PUT", {
                    "content": stReport.value,
                    "sprint_objective": spObj.value,
                    "user_story": userStory.value,
                    "status": statusStr
                })
            })
        })
        
    }
    
    
})


