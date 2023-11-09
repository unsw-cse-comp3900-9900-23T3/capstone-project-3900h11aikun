import { doFetch } from "../helper.js";
const home = document.getElementById('home');
const myPro = document.getElementById('mypro');
const profile = document.getElementById('profile');
const logout = document.getElementById('logout');
const findSt = document.getElementById('findSt');
const revise = document.getElementById('revise');
const requireSkills = document.getElementById('requireSkills');
const problemStatement = document.getElementById('problemStatement');
const desiredOutcome = document.getElementById('desiredOutcome');
const projectName = document.getElementById('projectName');
console.log(projectName);
const contact = document.getElementById('contact');
const urlParams = new URLSearchParams(window.location.search);
const project_id = Number(urlParams.get('id'));
// interaction display
function naviDisplay (item) {
    item.addEventListener('mouseover', (event) => {
        item.style.color = `rgb(${0}, ${193}, ${193})`;
    });
    item.addEventListener('mouseleave', (event) => {
        item.style.color = 'white';
    });
};

findSt.addEventListener('mouseover', (event) => {
    findSt.style.background = `rgb(${0}, ${220}, ${220})`;
});
findSt.addEventListener('mouseleave', (event) => {
    findSt.style.background = `rgb(${0}, ${193}, ${193})`;
});
findSt.addEventListener('click', (event) => {
    console.log(findSt.value)
    if (findSt.value === 'project is in progress') {
        alert('to sp3 page')
    } else {
        window.location.href = "../stSuListForBoss/BviewApplication.html?projectId=" + project_id;
    }

});
const roleId = Number(localStorage.getItem('roleId'));

revise.addEventListener('mouseover', (event) => {
    revise.style.color = `rgb(${0}, ${230}, ${230})`;
});
revise.addEventListener('mouseleave', (event) => {
    revise.style.color = `rgb(${0}, ${193}, ${193})`;
});



revise.addEventListener('click', (event) => {
    window.location.href = "../PostProject/postProject.html?projectId=" + project_id;
});

doFetch('/profile/project?project_id=' + project_id, "GET").then((data)=>{
    console.log(data)
    const currProj = data[0];
    requireSkills.textContent = currProj.required_skills;
    problemStatement.textContent = currProj.problem_statement;
    desiredOutcome.textContent = currProj.desired_outcomes;
    potentialDeliverable.textContent = currProj.deliverables;
    projectName.textContent = currProj.title;
    console.log(currProj.student_id)
    if (currProj.student_id !== null && currProj.supervisor_id !== null) {
        console.log('hiii')
        findSt.value = 'project is in progress';
    } else if (currProj.student_id !== null) {
        findSt.value = 'Recommand and applied supervisor'
        findSt.style.width = '370px';
    }
    
    doFetch('/profile/partner?partner_id=' + currProj.partner_id, 'GET').then((partnerInfo) => {
        console.log(partnerInfo[0]);
        contact.textContent = partnerInfo[0].email;
    })
})

naviDisplay(home);
naviDisplay(myPro);
naviDisplay(profile);
naviDisplay(logout);

logout.addEventListener('click', ()=>{
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('roleId');
    localStorage.removeItem('username');
    localStorage.removeItem('password');
})

