import { doFetch } from "../helper.js";

const home = document.getElementById('home');
const myPro = document.getElementById('mypro');
const logout = document.getElementById('logout');
const firstName = document.getElementById('firstName');
const lastName = document.getElementById('lastName');
const company = document.getElementById('company');
const email = document.getElementById('email');
const submit = document.getElementById('submit');
const roleId = Number(localStorage.getItem('roleId')); 

// make button color change when mouse over
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

// modify partner's profile when user click submit
submit.addEventListener('click', (event) => {
    if (submit.value === 'Submit') {
        doFetch('/profile/partner', 'PUT', {
            "partner_id": roleId,
            "first_name": firstName.value,
            "last_name": lastName.value,
            "email": email.value,
            "company": company.value
        }).then((pInfo)=>{
            firstName.value = pInfo.first_name;
            lastName.value = pInfo.last_name;
            company.value = pInfo.company;
            email.value = pInfo.email;
        })
        submit.value = 'Edit';
        firstName.disabled = true;
        lastName.disabled = true;
        company.disabled = true;
    } else {
        submit.value = 'Submit';
        firstName.disabled = false;
        lastName.disabled = false;
        company.disabled = false;
    }
    
});
naviDisplay(home);
naviDisplay(myPro);
naviDisplay(logout);
inputDisplay(firstName);
inputDisplay(lastName);
inputDisplay(company);
inputDisplay(email);


// get partner's originaol info
doFetch('/profile/partner?partner_id=' + roleId, 'GET').then((data)=>{
    const pInfo = data[0];
    firstName.value = pInfo.first_name;
    lastName.value = pInfo.last_name;
    company.value = pInfo.company;
    email.value = pInfo.email;
})

logout.addEventListener('click', ()=>{
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('roleId');
    localStorage.removeItem('username');
    localStorage.removeItem('password');
})