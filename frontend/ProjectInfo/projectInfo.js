import { doFetch } from "../helper.js";

const home = document.getElementById('home');
const myPro = document.getElementById('mypro');
const apply = document.getElementById('apply');
const profile = document.getElementById('profile');
const logout = document.getElementById('logout');
const applyButton = document.getElementById('applyButton');
const improve = document.getElementById('improve');
const requireSkills = document.getElementById('requireSkills');
const problemStatement = document.getElementById('problemStatement');
const desiredOutcome = document.getElementById('desiredOutcome');
const projectName = document.getElementById('projectName');
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



applyButton.addEventListener('mouseover', (event) => {
    applyButton.style.background = `rgb(${0}, ${220}, ${220})`;
});
applyButton.addEventListener('mouseleave', (event) => {
    applyButton.style.background = `rgb(${0}, ${193}, ${193})`;
});

improve.addEventListener('mouseover', (event) => {
    improve.style.color = `rgb(${0}, ${230}, ${230})`;
});
improve.addEventListener('mouseleave', (event) => {
    improve.style.color = `rgb(${0}, ${193}, ${193})`;
});

naviDisplay(home);
naviDisplay(myPro);
naviDisplay(apply);
naviDisplay(profile);
naviDisplay(logout);
const urlParams = new URLSearchParams(window.location.search);
const project_id = urlParams.get('id');
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

let roleString = '';
let role = localStorage.getItem('role');
if (role === 'student') {
    roleString = 'student_id';
} else if (role === 'supervisor') {
    roleString = 'supervisor_id';
} else {
    alert('in valid role using this function');
}
let applied = false;
const roleId = localStorage.getItem('roleId');
doFetch(`/profile/project/interest/${role}?project_id=${project_id}&${roleString}=${roleId}`, 'GET').then((data) => {
    console.log(data)
    if (data.length === 0) {
        applyButton.value = 'Apply now';

    } else {
        applyButton.value = 'Cancel application';
        applyButton.style.width = '250px';
        applied = true;
    }
})
applyButton.addEventListener('click', ()=>{
    console.log(applied)
    if (applied) {
        doFetch('/profile/project/interest/' + role, 'DELETE', {'project_id': Number(project_id), [roleString]: Number(localStorage.getItem('roleId'))}).then((data) => {
            console.log(data)
            applyButton.value = 'Apply now';
            applied = false;
            applyButton.style.width = '200px';
        })
    } else {
        doFetch('/profile/project/interest/' + role, 'POST', {'project_id': Number(project_id), [roleString]: Number(localStorage.getItem('roleId'))}).then((data) => {
            console.log(data);
            applyButton.value = 'Cancel application';
            applyButton.style.width = '250px';
            applied = true;
        });
    }
    window.location.href = "../stSuApplication/stSuApplication.html";
})
let userRole = localStorage.getItem('role');
document.getElementById('pdfUploader').addEventListener('change', (event)=> {
    let file = event.target.files[0];

    if (!file) {
        console.log("No file selected.");
        return;
    }

    // Check if the file is a PDF
    if (file.type !== "application/pdf") {
        console.log("Please select a PDF file.");
        return;
    }

    // Create FormData and append the file
    let formData = new FormData();
    formData.append("file", file, file.name);

    let stSuUrl = '/supervisorInfo/supervisor_upload_resume';
    if (userRole === 'student') {
        stSuUrl = '/studentInfo/student_upload_resume/';
    }
    let roleId = localStorage.getItem('roleId');
    // doFetch(stSuUrl + roleId, 'POST', formData);
    fetch('http://localhost:9998' + stSuUrl + roleId, {
        method: "POST",
        body: formData,
      })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
});
improve.addEventListener("click", function() {
    document.getElementById("pdfUploader").click();
});