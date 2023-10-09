const student = document.getElementById('student');
const supervisor = document.getElementById('supervisor');
const partner = document.getElementById('partner');
const comment1 = document.getElementById('commentone');
const comment2 = document.getElementById('commenttwo');
const comment3 = document.getElementById('commentthree');
const username = document.getElementById('username');
const password = document.getElementById('password')
const submit = document.getElementById('submit');
const passerror = document.getElementById('passerror');
const register = document.getElementById('register');

student.style.background = 'white';
student.style.color = `rgb(${0}, ${193}, ${193})`


function identityMouseDisplay(identity) {
    identity.addEventListener('mouseover', (event) => {
        identity.style.color = `rgb(${0}, ${193}, ${193})`;
    });
    identity.addEventListener('mouseleave', (event) => {
        if (identity.style.background != 'white') {
            identity.style.color = 'black';
        }
    });
}
function infoMouseDisplay(info) {
    info.addEventListener('mouseover', (event) => {
        info.style.borderColor = `rgb(${0}, ${193}, ${193})`;
    })
    info.addEventListener('mouseleave', (event) => {
        info.style.borderColor = `rgb(${217}, ${217}, ${217})`;
    })
}
identityMouseDisplay(student);
identityMouseDisplay(supervisor);
identityMouseDisplay(partner);
infoMouseDisplay(username);
infoMouseDisplay(password);


student.addEventListener('click', (event) => {
    student.style.color = `rgb(${0}, ${193}, ${193})`;
    student.style.background = 'white';
    supervisor.style.color = 'black';
    supervisor.style.background = `rgb(${245}, ${245}, ${245})`
    partner.style.color = 'black';
    partner.style.background = `rgb(${245}, ${245}, ${245})`
    comment1.innerHTML = 'Find & participate in projects';
    comment2.innerHTML = 'Professional guidance & help';
    comment3.innerHTML = 'Get accurate recommendations';
});
supervisor.addEventListener('click', (event) => {
    supervisor.style.color = `rgb(${0}, ${193}, ${193})`;
    supervisor.style.background = 'white';
    student.style.color = 'black';
    student.style.background = `rgb(${245}, ${245}, ${245})`
    partner.style.color = 'black';
    partner.style.background = `rgb(${245}, ${245}, ${245})`
    comment1.innerHTML = 'Find & participate in projects';
    comment2.innerHTML = 'Work with excelent students';
    comment3.innerHTML = 'Get accurate recommendations';
});
partner.addEventListener('click', (event) => {
    partner.style.color = `rgb(${0}, ${193}, ${193})`;
    partner.style.background = 'white';
    student.style.color = 'black';
    student.style.background = `rgb(${245}, ${245}, ${245})`
    supervisor.style.color = 'black';
    supervisor.style.background = `rgb(${245}, ${245}, ${245})`
    comment1.innerHTML = 'Post projects more efficient';
    comment2.innerHTML = 'excellent students & supervisor';
    comment3.innerHTML = 'Get accurate recommendations';
});


submit.addEventListener('mouseover', (event) => {
    submit.style.background = `rgba(${1}, ${173}, ${173}, ${0.8})`
})
submit.addEventListener('mouseleave', (event) => {
    submit.style.background = `rgb(${1}, ${173}, ${173})`
})


register.addEventListener('mouseover', (event) => {
    register.style.color = `rgb(${1}, ${173}, ${173})`;
})
register.addEventListener('mouseleave', (event) => {
    register.style.color = 'black';
})


submit.addEventListener('click', (event) => {
    // username not exist
    // email not exist
    // wrong password
    // wrong identity, click to create account
});


