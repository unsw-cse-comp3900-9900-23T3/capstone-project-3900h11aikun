import { doFetch } from "../helper.js";

const home = document.getElementById('home');
const myPro = document.getElementById('mypro');
const profile = document.getElementById('profile');
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
naviDisplay(profile);
naviDisplay(logout);

function newPro (title, proStatus, project_id) {
    const project = document.createElement('div');
    project.className = 'project';
    projects.appendChild(project);

    const name = document.createElement('div');
    name.textContent = title;
    name.className = 'name';
    project.appendChild(name);

    const status = document.createElement('div');
    status.textContent = proStatus;
    status.className = 'status';
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

const partnerId = localStorage.getItem('roleId');
doFetch(`/profile/project?partner_id=${partnerId}`, 'GET').then((projs)=>{
    projs.forEach((proj)=>{
        newPro(proj.title, proj.status, proj.project_id);
    })
})