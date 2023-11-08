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
const urlParams = new URLSearchParams(window.location.search);
const bossView = urlParams.has('studentId');
const bossViewSId = urlParams.get('studentId');

if (bossView) {
    console.log('yoo')
    ret.addEventListener('click', function() {
        window.history.back();
    });
}
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

const student_id = Number(localStorage.getItem('roleId'));
let sendSid = student_id;
if (bossView) {
    sendSid = bossViewSId;
}
console.log(`/studentInfo/getStudentInfo/{${sendSid}}`);
let url = `/studentInfo/getStudentInfo/${sendSid}`;
const role = localStorage.getItem('role');
if (role === "supervisor") {
    console.log('hii')
    stOrSu.textContent = "Supervisor Information";
    url=`/profile/supervisor?supervisor_id=${sendSid}`;
}
let resumeURL = null;
let quaOrStrength = "strength";
    if(role === 'supervisor') {
        quaOrStrength = "qualification";
    }
doFetch(url, 'GET').then((data1)=>{
    console.log(data1);
    let data = data1;
    if(role === 'supervisor') {
        data = data1[0];
    }
    skill.textContent = data.skills;
    name.textContent = data.first_name + ' ' + data.last_name;
    email.textContent = data.email;
    strength.textContent = data[quaOrStrength];
    resumeURL = data.resume_url;
})

view.addEventListener('click', ()=>{
    window.open(resumeURL, '_blank');
})

logout.addEventListener('click', ()=>{
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('roleId');
    localStorage.removeItem('username');
    localStorage.removeItem('password');
})
