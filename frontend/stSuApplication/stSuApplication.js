import { doFetch } from "../helper.js";

const home = document.getElementById('home');
const myPro = document.getElementById('mypro');
const apply = document.getElementById('apply');
const profile = document.getElementById('profile');
const logout = document.getElementById('logout');
const ret = document.getElementById('return');
const applications = document.getElementById('applications');


// Interaction display
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
naviDisplay(apply);
naviDisplay(profile);
naviDisplay(logout);


// Example of applied projects
function createAppllication (pStatus, updateTime, pTitle, contacter, project_id) {
    const project = document.createElement('div');
    project.style.background = 'white';
    project.style.height = '150px';
    project.style.width = '800px';
    project.style.marginTop = '20px';
    project.style.borderRadius = '10px';
    applications.appendChild(project);

    const partnerInfo = document.createElement('div');
    partnerInfo.style.display = 'flex';
    partnerInfo.style.height = '50px';
    partnerInfo.style.background = `rgba(${128}, ${128}, ${128}, ${0.3})`;
    partnerInfo.style.borderTopLeftRadius = '10px';
    partnerInfo.style.borderTopRightRadius = '10px';
    project.appendChild(partnerInfo);

    const partner = document.createElement('div');
    partner.style.width = '560px';
    partner.textContent = `Status: ${pStatus} | Updated at: ${updateTime}`;
    partner.style.fontSize = '1.1em';
    partner.style.lineHeight = '50px';
    partner.style.marginLeft = '25px';
    partnerInfo.appendChild(partner);

    const viewMore = document.createElement('input');
    viewMore.type = 'button';
    viewMore.value = 'View More';
    viewMore.style.marginLeft = '10px';
    viewMore.style.width = '150px';
    viewMore.style.color = 'white';
    viewMore.style.border = '0px';
    viewMore.style.background = `rgb(${0}, ${193}, ${193})`;
    viewMore.style.borderRadius = '10px';
    viewMore.style.height = '40px';
    viewMore.style.marginTop = '5px';
    viewMore.addEventListener('mouseover', (event) => {
        viewMore.style.background = `rgb(${0}, ${170}, ${170})`;
        viewMore.style.color = 'black';
    });
    viewMore.addEventListener('mouseleave', (event) => {
        viewMore.style.background = `rgb(${0}, ${193}, ${193})`;
        viewMore.style.color = 'white';
    });

    viewMore.addEventListener('click', (event) => {
        window.location.href = '../ProjectInfo/projectInfo.html' + '?id=' + project_id;
    });

    partnerInfo.appendChild(viewMore);

    const proTitle = document.createElement('div');
    proTitle.textContent = pTitle;
    proTitle.style.marginLeft = '25px';
    proTitle.style.marginTop = '15px';
    proTitle.style.fontSize = '1.2em';
    project.appendChild(proTitle);

    const proInfo = document.createElement('div');
    proInfo.style.display = 'flex';
    proInfo.style.marginLeft = '25px';
    project.appendChild(proInfo);

    const contact = document.createElement('div');
    contact.textContent = 'Contact:';
    contact.style.marginLeft = '0px';
    contact.style.marginTop = '15px';
    contact.style.fontWeight = 'bold';
    proInfo.appendChild(contact);

    const email = document.createElement('div');
    email.textContent = contacter;
    email.style.marginLeft = '20px';
    email.style.marginTop = '15px';
    email.style.fontSize = '0.9em';
    proInfo.appendChild(email);
}

createAppllication();
let roleString = '';
const roleId = localStorage.getItem('roleId');
let role = localStorage.getItem('role');
if (role === 'student') {
    roleString = 'student_id';
} else if (role === 'supervisor') {
    roleString = 'supervisor_id';
} else {
    alert('in valid role using this function');
}

doFetch(`/profile/project/interest/${role}?${roleString}=${roleId}`, 'GET').then((data)=>{

    data.forEach(proj => {
        doFetch('/profile/project?project_id=' + proj.project_id, 'GET').then((currProjLi)=>{
            const projInfo = currProjLi[0];
            console.log(projInfo)
            doFetch('/profile/partner?partner_id=' + projInfo.partner_id, 'GET').then((partnerInfo) => {
                console.log(partnerInfo[0]);
                createAppllication(projInfo.status, projInfo.project_last_updated_at, projInfo.title, partnerInfo[0].email, proj.project_id);
            })
            
        })
    });
    
});