import { doFetch } from "../helper.js";
const home = document.getElementById('home');
const myPro = document.getElementById('mypro');
const profile = document.getElementById('profile');
const logout = document.getElementById('logout');
const ret = document.getElementById('return');
const recommand = document.getElementById('recommand');
const applied = document.getElementById('applied');
const RStSu = document.getElementById('RStSu');
const BossBar = document.getElementById('BossBar');
const AStSu = document.getElementById('AStSu');
const studentBar = document.getElementById('studentBar');
const urlParams = new URLSearchParams(window.location.search);
const project_id = urlParams.get('projectId');

let isStudent = true;
// Interaction display
function naviDisplay (item) {
    item.addEventListener('mouseover', (event) => {
        item.style.color = `rgb(${0}, ${193}, ${193})`;
    });
    item.addEventListener('mouseleave', (event) => {
        item.style.color = 'white';
    });
};

ret.addEventListener('mouseover', (event) => {
    ret.style.background = `rgb(${0}, ${193}, ${193})`;
    ret.style.color = 'white';
});
ret.addEventListener('mouseleave', (event) => {
    ret.style.background = 'white';
    ret.style.color = 'black';
});
ret.addEventListener('click', (event) => {
    window.history.back();
});

function buttonDisplay (item) {
    item.addEventListener('mouseover', (event) => {
        item.style.background = `rgb(${0}, ${220}, ${220})`;
    });
    item.addEventListener('mouseleave', (event) => {
        item.style.background = `rgb(${0}, ${193}, ${193})`;
    });
};

naviDisplay(home);
naviDisplay(myPro);
naviDisplay(profile);
naviDisplay(logout);
let role = localStorage.getItem('role');
if (role === 'student') {
    BossBar.classList.add('hide');
    studentBar.classList.remove('hide');
}

// Example of insert student
function loadStudent(part, nameContent, education, stId) {
    const student = document.createElement('div');
    student.className = 'student';
    part.appendChild(student);

    const name = document.createElement('div');
    name.className = 'name';
    name.textContent = nameContent;
    student.appendChild(name);

    const edu = document.createElement('div');
    edu.className = 'edu';
    edu.textContent = education;
    student.appendChild(edu);

    const button = document.createElement('input');
    button.type = 'button';
    button.className = 'viewmore';
    button.value = 'View more';
    if (part === applied) {
        const selectButton = document.createElement('input');
        selectButton.type = 'button';
        selectButton.className = 'viewmore';
        selectButton.value = 'Add person to project';
        if (role !== 'student') {
            student.appendChild(selectButton);
            buttonDisplay(selectButton);
            student.style.height = '170px';
        }
        
        selectButton.addEventListener("click", ()=>{
            doFetch('/profile/project?project_id=' + project_id, "GET").then((data)=>{
                let stSu = "student_id";
                const currProj = data[0];
                if (!isStudent) {
                    stSu = 'supervisor_id';
                }
                currProj[stSu] = stId;
                doFetch('/profile/project', 'PUT', currProj);
            })
            window.location.href = "../BossProject/BProjectInfo.html" + '?id=' + project_id;
        })
    }
    
    button.addEventListener('click', ()=>{
        let stSu = 'studentId';
        if (!isStudent) {
            stSu = 'supervisorId';
        }
        window.location.href = `../stSuInfo/stSuinfo.html?${stSu}=${stId}`;
    })
    student.appendChild(button);
    
    buttonDisplay(button);
    
};

console.log(project_id)
doFetch('/profile/project?project_id=' + project_id, 'GET').then((data)=>{
    
    console.log(data)
    const currProj = data[0];
    console.log(currProj);
    
    if (currProj.student_id != null) {
        isStudent = false;
        RStSu.textContent = 'Recommand Supervisors';
        AStSu.textContent = 'Applied Supervisors';
        doFetch('/profile/supervisor?skills=' + currProj.required_skills, 'GET').then((data2) => {
            console.log(data2);
            data2.forEach((student)=>{
                doFetch('/profile/supervisor?supervisor_id=' + student.supervisor_id).then((data)=>{
                    loadStudent(recommand, student.first_name + ' ' + student.last_name, data[0].email, data[0].supervisor_id);
                })
            })
        })
        doFetch('/profile/project/interest/supervisor?project_id=' + project_id, 'GET').then((data2) => {
            console.log(data2);
            data2.forEach((student)=>{
                doFetch('/profile/supervisor?supervisor_id=' + student.supervisor_id).then((data)=>{
                    loadStudent(applied, student.first_name + ' ' + student.last_name, data[0].email, data[0].supervisor_id);
                })
            })
        })
    } else {
        doFetch('/profile/student?skills=' + currProj.required_skills, 'GET').then((data2) => {
            console.log(data2);
            data2.forEach((student)=>{
                doFetch('/profile/student?student_id=' + student.student_id).then((data)=>{
                    loadStudent(recommand, student.first_name + ' ' + student.last_name, data[0].email, data[0].student_id);
                })
            })
        })
        doFetch('/profile/project/interest/student?project_id=' + project_id, 'GET').then((data2) => {
            console.log(data2);
            data2.forEach((student)=>{
                doFetch('/profile/student?student_id=' + student.student_id).then((data)=>{
                    loadStudent(applied, student.first_name + ' ' + student.last_name, data[0].email, data[0].student_id);
                })
            })
        })
    }
})



logout.addEventListener('click', ()=>{
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('roleId');
    localStorage.removeItem('username');
    localStorage.removeItem('password');
})