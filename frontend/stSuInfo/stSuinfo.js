import { doFetch } from "../helper.js";

const home = document.getElementById('home');
const myPro = document.getElementById('mypro');
const profile = document.getElementById('profile');
const logout = document.getElementById('logout');
const ret = document.getElementById('return');
const view = document.getElementById('view');
const skill = document.getElementById('skill');
const name = document.getElementById('name');
const email = document.getElementById('email');
const strength = document.getElementById('strength');
const stOrSu = document.getElementById('stOrSu');


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
    window.location.href = "../HomeDir/home.html";
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
buttonDisplay(view);

const student_id = localStorage.getItem('roleId');
console.log(`/studentInfo/getStudentInfo/{${student_id}}`);
let url = `/studentInfo/getStudentInfo/${student_id}`;
const role = localStorage.getItem('role');
if (role === "supervisor") {
    stOrSu.value = "Supervisor Information";
    url=`/profile/supervisor?supervisor_id=${student_id}`;
}
let resumeURL = null;
doFetch(url, 'GET').then((data1)=>{
    console.log(data1);
    let data = data1;
    if(role === 'supervisor') {
        data = data1[0];
    }
    skill.textContent = data.skills;
    name.textContent = data.first_name + ' ' + data.last_name;
    email.textContent = data.email;
    strength.textContent = data.qualification;
    resumeURL = data.resume_url;
})

view.addEventListener('click', ()=>{
    window.open(resumeURL, '_blank');
})

