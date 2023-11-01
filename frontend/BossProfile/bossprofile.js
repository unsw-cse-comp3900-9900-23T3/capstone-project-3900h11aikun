const home = document.getElementById('home');
const myPro = document.getElementById('mypro');
const profile = document.getElementById('profile');
const logout = document.getElementById('logout');
const firstName = document.getElementById('firstName');
const lastName = document.getElementById('lastName');
const company = document.getElementById('company');
const email = document.getElementById('email');
const submit = document.getElementById('submit');

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

submit.addEventListener('mouseover', (event) => {
    submit.style.background = `rgb(${0}, ${220}, ${220})`;
});
submit.addEventListener('mouseleave', (event) => {
    submit.style.background =  `rgb(${0}, ${193}, ${193})`;
});

naviDisplay(home);
naviDisplay(myPro);
naviDisplay(profile);
naviDisplay(logout);
inputDisplay(firstName);
inputDisplay(lastName);
inputDisplay(company);
inputDisplay(email);
