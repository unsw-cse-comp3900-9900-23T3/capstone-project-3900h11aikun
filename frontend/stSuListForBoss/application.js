const home = document.getElementById('home');
const myPro = document.getElementById('mypro');
const profile = document.getElementById('profile');
const logout = document.getElementById('logout');
const ret = document.getElementById('return');
const recommand = document.getElementById('recommand');
const applied = document.getElementById('applied');


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


// Example of insert student
function loadStudent(part, nameContent, education) {
    const student = document.createElement('div');
    student.className = 'student';
    part.appendChild(student);

    const name = document.createElement('div');
    name.className = 'name';
    name.textContent = nameContent;
    student.appendChild(name);

    const edu = document.createElement('div');
    edu.className = 'edu';
    edu.textContent = education;
    student.appendChild(edu);

    const button = document.createElement('input');
    button.type = 'button';
    button.className = 'viewmore'
    button.value = 'View More';
    student.appendChild(button);
    buttonDisplay(button);
};

loadStudent(recommand, 'Student Name', 'postgraduate');
loadStudent(recommand, 'Student Name', 'postgraduate');
loadStudent(recommand, 'Student Name', 'postgraduate');
loadStudent(recommand, 'Student Name', 'postgraduate');
loadStudent(recommand, 'Student Name', 'postgraduate');


loadStudent(applied, 'Student Name', 'postgraduate');
loadStudent(applied, 'Student Name', 'postgraduate');
loadStudent(applied, 'Student Name', 'postgraduate');
loadStudent(applied, 'Student Name', 'postgraduate');
loadStudent(applied, 'Student Name', 'postgraduate');

