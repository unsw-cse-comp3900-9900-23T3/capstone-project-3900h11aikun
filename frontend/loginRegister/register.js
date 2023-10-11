const student = document.getElementById('student');
const supervisor = document.getElementById('supervisor');
const partner = document.getElementById('partner');
const comment1 = document.getElementById('commentone');
const comment2 = document.getElementById('commenttwo');
const comment3 = document.getElementById('commentthree');
const username = document.getElementById('username');
const email = document.getElementById('email');
const password = document.getElementById('password')
const submit = document.getElementById('submit');
const passerror = document.getElementById('passerror');
const emailerror = document.getElementById('emalerr');
const backendError = document.getElementById('backendError');

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
infoMouseDisplay(email);
infoMouseDisplay(password);

let roleType = 'student';
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
    roleType = 'student';
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
    roleType = 'supervisor';
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
    roleType = 'partner';
});


submit.addEventListener('mouseover', (event) => {
    submit.style.background = `rgba(${1}, ${173}, ${173}, ${0.8})`
})
submit.addEventListener('mouseleave', (event) => {
    submit.style.background = `rgb(${1}, ${173}, ${173})`
})

submit.addEventListener('click', (event) => {
    event.preventDefault();
    const homePageLink = event.currentTarget.href;
    passerror.innerHTML = '';
    emailerror.innerHTML = '';
    // email format checking
    backendError.textContent = '';
    let hasError = false;
    if (email.value.length < 7 || email.value.includes('@') == false) {
        emailerror.innerHTML = 'Please input a valid email';
        hasError = true;
    }
    console.log(hasError)

    let uperr = true;
    let lwerr = true;
    let nuerr = true;
    let syerr = true;
    for (let i = 0; i < password.value.length; i++) {
        char = password.value[i];
        if (char >= 'A' && char <= 'Z') {
            uperr = false;
        } else if (char >= 'a' && char <= 'z') {
            lwerr = false;
        } else if (char >= 0 && char <= 9) {
            nuerr = false;
        } else if ("[ *$&#/\t\n\f\”\'\\,.:;?!\[\](){}<>~\-_]".includes(char) == true) {
            syerr = false;    
        } else {
            hasError = true;
        }
    }
    if (password.value.length < 8) {
        passerror.innerHTML = 'Password can not be shorter than 8 characters';
        hasError = true;
    } else if (uperr == true) {
        passerror.innerHTML = 'Password must contain upper case word';
    } else if(lwerr == true) {
        passerror.innerHTML = 'password must contain lower case word';
    } else if (nuerr == true) {
        passerror.innerHTML = 'password must contain number';
    } else if (syerr == true) {
        passerror.innerHTML = 'password must contain symbol';
    } else if (!hasError) {
        // detail information for fetch, contain data send to backend
        const options = {
            method:'POST',
            headers: {
                'Content-Type':'application/json; charset=UTF-8'
            },
            body: JSON.stringify({
                'username': username.value,
                "password": password.value,
                "email": email.value,
                "type": roleType
            })

        };
        
        fetch('http://localhost:9998/auth/register', options).then(resp =>{
            return resp.json();
        }).then(data => {
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
});

