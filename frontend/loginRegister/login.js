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
    if (!info) return;
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

let roleType = 'student';
student.addEventListener('click', (event) => {
    student.style.color = `rgb(${0}, ${193}, ${193})`;
    student.style.background = 'white';
    supervisor.style.color = 'black';
    supervisor.style.background = `rgb(${245}, ${245}, ${245})`
    partner.style.color = 'black';
    partner.style.background = `rgb(${245}, ${245}, ${245})`
    comment1.textContent = 'Find & participate in projects';
    comment2.textContent = 'Professional guidance & help';
    comment3.textContent = 'Get accurate recommendations';
    roleType = 'student';
});
supervisor.addEventListener('click', (event) => {
    supervisor.style.color = `rgb(${0}, ${193}, ${193})`;
    supervisor.style.background = 'white';
    student.style.color = 'black';
    student.style.background = `rgb(${245}, ${245}, ${245})`
    partner.style.color = 'black';
    partner.style.background = `rgb(${245}, ${245}, ${245})`
    comment1.textContent = 'Find & participate in projects';
    comment2.textContent = 'Work with excelent students';
    comment3.textContent = 'Get accurate recommendations';
    roleType = 'supervisor';
});
partner.addEventListener('click', (event) => {
    partner.style.color = `rgb(${0}, ${193}, ${193})`;
    partner.style.background = 'white';
    student.style.color = 'black';
    student.style.background = `rgb(${245}, ${245}, ${245})`
    supervisor.style.color = 'black';
    supervisor.style.background = `rgb(${245}, ${245}, ${245})`
    comment1.textContent = 'Post projects more efficient';
    comment2.textContent = 'excellent students & supervisor';
    comment3.textContent = 'Get accurate recommendations';
    roleType = 'partner';
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
    // detail information for fetch, contain data send to backend
    event.preventDefault();
    const homePageLink = event.currentTarget.href;
    console.log('yyyy');
    if (username.value.includes('@')) {
    
        fetchInLogin('/auth/login_with_email', 'email', homePageLink);
    } else {
        fetchInLogin('/auth/login', 'username', homePageLink);
    }
    
});

function fetchInLogin(url, emailOrUsername, homePageLink) {
    options = {
        "password": password.value,
        "type": roleType
    }
    options[emailOrUsername] = username.value;
    doFetch(url, 'POST', options).then(data => {
        if (data.message) {
            // if data have message key means something 
            // wrong, we give user a warning to tell them try again
            backendError.textContent = 'Warning: ' + data.message;
        } else {
            // if there is no error, registeration successful, navigate to home page
            window.location.href = homePageLink;
        }
    })
}

function doFetch(url, method, body) {
    
    let options = {};
    options.method = method;
    // body contains detail information for fetch, data will be sent to backend
    if (body) {
        options.headers = {
            'Content-Type':'application/json; charset=UTF-8'
        };
        options.body = JSON.stringify(body);
    }
    
    return fetch('http://localhost:9998' + url, options).then(resp =>{
        console.log('http://localhost:9998' + url)
        return resp.json();
    })

}
