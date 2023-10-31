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
    window.location.href = "../stSuListForBoss/BviewApplication.html";

});
revise.addEventListener('mouseover', (event) => {
    revise.style.color = `rgb(${0}, ${230}, ${230})`;
});
revise.addEventListener('mouseleave', (event) => {
    revise.style.color = `rgb(${0}, ${193}, ${193})`;
});

const urlParams = new URLSearchParams(window.location.search);
const project_id = urlParams.get('id');

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
    doFetch('/profile/partner?partner_id=' + currProj.partner_id, 'GET').then((partnerInfo) => {
        console.log(partnerInfo[0]);
        contact.textContent = partnerInfo[0].email;
    })
})

naviDisplay(home);
naviDisplay(myPro);
naviDisplay(profile);
naviDisplay(logout);



