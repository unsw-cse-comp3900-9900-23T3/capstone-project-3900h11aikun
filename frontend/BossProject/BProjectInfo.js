const home = document.getElementById('home');
const myPro = document.getElementById('mypro');
const profile = document.getElementById('profile');
const logout = document.getElementById('logout');
const find = document.getElementById('find');
const revise = document.getElementById('revise');


// interaction display
function naviDisplay (item) {
    item.addEventListener('mouseover', (event) => {
        item.style.color = `rgb(${0}, ${193}, ${193})`;
    });
    item.addEventListener('mouseleave', (event) => {
        item.style.color = 'white';
    });
};

find.addEventListener('mouseover', (event) => {
    find.style.background = `rgb(${0}, ${220}, ${220})`;
});
find.addEventListener('mouseleave', (event) => {
    find.style.background = `rgb(${0}, ${193}, ${193})`;
});

revise.addEventListener('mouseover', (event) => {
    revise.style.color = `rgb(${0}, ${230}, ${230})`;
});
revise.addEventListener('mouseleave', (event) => {
    revise.style.color = `rgb(${0}, ${193}, ${193})`;
});

naviDisplay(home);
naviDisplay(myPro);
naviDisplay(profile);
naviDisplay(logout);

