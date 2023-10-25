const home = document.getElementById('home');
const myPro = document.getElementById('mypro');
const apply = document.getElementById('apply');
const profile = document.getElementById('profile');
const logout = document.getElementById('logout');
const name = document.getElementById('name');
const age = document.getElementById('age');
const email = document.getElementById('email');
const edu = document.getElementById('edu');
const school = document.getElementById('school');
const java = document.getElementById('java');
const python = document.getElementById('python');
const js = document.getElementById('js');
const c = document.getElementById('c');
const ml = document.getElementById('ml');
const dl = document.getElementById('dl');
const sd = document.getElementById('sd');
const net = document.getElementById('net');
const data = document.getElementById('data');
const strength = document.getElementById('strength');
const strengthInput = document.getElementById('strengthInput');
const experience = document.getElementById('experience');
const experienceInput = document.getElementById('experienceInput');
const upload = document.getElementById('upload');
const dele = document.getElementById('delete');
const submit = document.getElementById('submit');


// Interaction display
function naviDisplay (item) {
    item.addEventListener('mouseover', (event) => {
        item.style.color = `rgb(${0}, ${193}, ${193})`;
    });
    item.addEventListener('mouseleave', (event) => {
        item.style.color = 'white';
    });
};

function inputDisplay (item) {
    item.addEventListener('mouseover', (event) => {
        item.style.borderColor = `rgb(${0}, ${193}, ${193})`;
    });
    item.addEventListener('mouseleave', (event) => {
        item.style.borderColor = `rgba(${128}, ${128}, ${128}, ${0.3})`;
    });
};

function skillDisplay (item) {
    item.addEventListener('mouseover', (event) => {
        item.style.background = `rgba(${0}, ${193}, ${193})`;
    });
    item.addEventListener('mouseleave', (event) => {
        if (item.style.color == 'white') {
            item.style.background = `rgb(${0}, ${193}, ${193})`;
        } else {
            item.style.background = `rgba(${128}, ${128}, ${128}, ${0.3})`;
        }
    });
    item.addEventListener('click', (event) => {
        if (item.style.color == 'black') {
            item.style.color = 'white';
            item.style.background = `rgb(${0}, ${193}, ${193})`;
        } else {
            item.style.color = 'black';
            item.style.background = `rgb(${0}, ${193}, ${193})`;
        };
    });
};

function extraDisplay (item1, item2) {
    item1.addEventListener('mouseover', (event) => {
        item1.style.background = `rgba(${0}, ${193}, ${193}, ${0.5})`;
        item2.style.background = 'white';
    });
    item1.addEventListener('mouseleave', (event) => {
        item1.style.background = 'white';
        item2.style.background = `rgba(${128}, ${128}, ${128}, ${0.1})`;
    });
};

function resumeDisplay (item) {
    item.addEventListener('mouseover', (event) => {
        item.style.background = `rgb(${0}, ${220}, ${220})`;
    });
    item.addEventListener('mouseleave', (event) => {
        item.style.background =  `rgb(${0}, ${193}, ${193})`;
    })
};

naviDisplay(home);
naviDisplay(myPro);
naviDisplay(apply);
naviDisplay(profile);
naviDisplay(logout);
inputDisplay(name);
inputDisplay(age);
inputDisplay(email);
inputDisplay(edu);
inputDisplay(school);
skillDisplay(java);
skillDisplay(python);
skillDisplay(js);
skillDisplay(c);
skillDisplay(ml);
skillDisplay(dl);
skillDisplay(sd);
skillDisplay(net);
skillDisplay(data);
extraDisplay(strength, strengthInput);
extraDisplay(experience, experienceInput);
resumeDisplay(upload);
resumeDisplay(dele);
resumeDisplay(submit);


// Can not use Form to submit
submit.addEventListener('click', (event) => {
    
})

