const home = document.getElementById('home');
const myPro = document.getElementById('mypro');
const apply = document.getElementById('apply');
const profile = document.getElementById('profile');
const logout = document.getElementById('logout');
const applyButton = document.getElementById('applyButton');
const improve = document.getElementById('improve');


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

