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
const download = document.getElementById('download');
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
buttonDisplay(download);
const student_id = localStorage.getItem('roleId');
console.log(`/studentInfo/getStudentInfo/{${student_id}}`);
if (localStorage.getItem('role') === "supervisor") {
    stOrSu = "Supervisor Information";
}
doFetch(`/studentInfo/getStudentInfo/${student_id}`, 'GET').then((data)=>{
    console.log(data);
    skill.textContent = data.skills;
    name.textContent = data.first_name + ' ' + data.last_name;
    email.textContent = data.email;
    strength.textContent = data.strength;
})


