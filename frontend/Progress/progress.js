const home = document.getElementById('home');
const myPro = document.getElementById('mypro');
const profile = document.getElementById('profile');
const logout = document.getElementById('logout');
const detail = document.getElementById('detail');
const add = document.getElementById('add');
const container = document.getElementById('container');
const dele = document.getElementById('delete');
const edit = document.getElementById('edit');
const upload = document.getElementById('upload');
const view = document.getElementById('view');
localStorage.setItem('numOfSprint', '0');
loadSprints(1);


// Interaction color display
function naviDisplay (item) {
    item.addEventListener('mouseover', (event) => {
        item.style.color = `rgb(${0}, ${193}, ${193})`;
    });
    item.addEventListener('mouseleave', (event) => {
        item.style.color = 'white';
    });
};

function buttonDisplay (item) {
    item.addEventListener('mouseover', (event) => {
        item.style.background = `rgb(${0}, ${230}, ${230})`;
    });
    item.addEventListener('mouseleave', (event) => {
        item.style.background = `rgb(${0}, ${193}, ${193})`;
    });
};

function sprintDisplay (item) {
    item.addEventListener('mouseover', (event) => {
        item.style.borderColor = `rgb(${0}, ${193}, ${193})`;
    });
    item.addEventListener('mouseleave', (event) => {
        item.style.borderColor = `rgba(${0}, ${0}, ${0}, ${0})`;
    });
};

add.addEventListener('mouseover', (event) => {
    add.style.color = `rgb(${0}, ${220}, ${220})`;
});
add.addEventListener('mouseleave', (event) => {
    add.style.color = `rgb(${0}, ${160}, ${160})`;
});

naviDisplay(home);
naviDisplay(myPro);
naviDisplay(profile);
naviDisplay(logout);
buttonDisplay(detail);
buttonDisplay(dele);
buttonDisplay(edit);
buttonDisplay(view);
buttonDisplay(upload);


// interaction dynamic display
add.addEventListener('click', (event) => {
    loadSprints(1);
});

function loadSprints (num) {
    for (let i = 1; i <= num; i++) {
        const number = Number(localStorage.getItem('numOfSprint')) + 1;
        const sprint = document.createElement('input');
        sprint.type = 'button'
        sprint.className = 'sprint';
        sprint.value = 'Sprint ' + number;
        if (number == 1) {
            sprint.style.color = 'white';
            sprint.style.background = `rgb(${0}, ${193}, ${193})`;
        };
        container.appendChild(sprint);
        sprintDisplay(sprint);
        clickSprint(sprint);
        localStorage.setItem('numOfSprint', number);
    };
};

function clickSprint (item) {
    item.addEventListener('click', (event) => {
        for (let i = 0; i < container.children.length; i++) {
            const child = container.children[i];
            child.style.background = 'white';
            child.style.color = `rgb(${0}, ${193}, ${193})`;
        };
        item.style.background = `rgb(${0}, ${193}, ${193})`;
        item.style.color = 'white';
    });
};








loadSprints(2);








