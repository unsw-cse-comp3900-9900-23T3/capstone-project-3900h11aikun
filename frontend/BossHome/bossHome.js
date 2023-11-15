import { doFetch } from "../helper.js";

const home = document.getElementById('home');
const myPro = document.getElementById('mypro');
const logout = document.getElementById('logout');
const projects = document.getElementById('projects');

function naviDisplay (item) {
    item.addEventListener('mouseover', (event) => {
        item.style.color = `rgb(${0}, ${193}, ${193})`;
    });
    item.addEventListener('mouseleave', (event) => {
        item.style.color = 'white';
    });
};

naviDisplay(home);
naviDisplay(myPro);
naviDisplay(logout);

// function for creating new project container
function newPro (title, proStatus, project_id) {
    const project = document.createElement('div');
    project.className = 'project';
    projects.appendChild(project);

    const name = document.createElement('div');
    name.textContent = title;
    name.className = 'name';
    name.style.overflow = 'auto';
    project.appendChild(name);

    const status = document.createElement('div');
    status.textContent = proStatus;
    status.className = 'status';
    if (proStatus === 'Finding student') {
        status.classList.add('themeBlack');
    } else if (proStatus === 'Finding supervisor') {
        status.classList.add('themeYellow');
    } else if (proStatus === 'Project in progress') {
        status.classList.add('themeGreen');
    }
    project.appendChild(status);

    const more = document.createElement('input');
    more.type = 'button';
    more.value = 'View More';
    more.className = 'viewMore'
    more.addEventListener('mouseover', (event) => {
        more.style.background = `rgb(${0}, ${193}, ${193})`;
        more.style.color = 'white';
    });
    more.addEventListener('mouseleave', (event) => {
        more.style.background = `rgb(${232}, ${235}, ${238})`;
        more.style.color = 'black';
    });
    more.addEventListener('click', (event) => {
        window.location.href = "../BossProject/BProjectInfo.html" + '?id=' + project_id;
    });

    project.appendChild(more);
}
// get projects contents
const partnerId = Number(localStorage.getItem('roleId'));
doFetch(`/profile/project?partner_id=${partnerId}`, 'GET').then((projs)=>{
    projs.forEach((proj)=>{
        console.log(proj)
        let pStatus = 'Finding student';
        if (proj.student_id !== null && proj.supervisor_id !== null) {
            pStatus = 'Project in progress';
        } else if (proj.student_id !== null) {
            pStatus = 'Finding supervisor';
        }
        newPro(proj.title, pStatus, proj.project_id);
    })
})
// logout button
logout.addEventListener('click', ()=>{
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('roleId');
    localStorage.removeItem('username');
    localStorage.removeItem('password');
})