import { doFetch } from "../helper.js";
const home = document.getElementById('home');
const myPro = document.getElementById('mypro');
const apply = document.getElementById('apply');
const profile = document.getElementById('profile');
const logout = document.getElementById('logout');
const name1 = document.getElementById('name');
const name2 = document.getElementById('name2');
const email = document.getElementById('email');
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
const upload = document.getElementById('upload');
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
inputDisplay(name1);
inputDisplay(name2);
inputDisplay(email);
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
resumeDisplay(upload);
resumeDisplay(submit);
const skillList = ['Java', 'Pthon', 'Javascript', 'C/C++', 'Machine Learning', 'Deep Learning', 'Software Develop', 'Networking', 'Database/Big Data'];
const student_id = localStorage.getItem('roleId');
console.log(`/studentInfo/getStudentInfo/{${student_id}}`);
let url = `/studentInfo/getStudentInfo/${student_id}`;
const role = localStorage.getItem('role');
if (role === "supervisor") {
    url=`/profile/supervisor?supervisor_id=${student_id}`;
}
doFetch(url, 'GET').then((data1)=>{
    let data = data1;
    console.log(data)
    let quaOrStrength = "strength";
    if(role === 'supervisor') {
        data = data1[0];
        quaOrStrength = "qualification";
    }
    name1.value = data.first_name;
    name2.value = data.last_name;
    email.value = data.email;
    strengthInput.value = data[quaOrStrength];
    if (skillList.includes(data.skill)) {
        const selectedEle = findSelectedEle(data.skill);
        selectedEle.classList.add('selected');
    }

})
function findSelectedEle(selectedString) {
    if (selectedString === 'Java') {
        return java;
    } else if (selectedString === 'Pthon') {
        return python;
    } else if (selectedString === 'Javascript') {
        return js;
    } else if (selectedString === 'C/C++') {
        return c;
    } else if (selectedString === 'Machine Learning') {
        return ml;
    } else if (selectedString === 'Deep Learning') {
        return dl;
    } else if (selectedString === 'Software Develop') {
        return sd;
    } else if (selectedString === 'Networking') {
        return net;
    } else if (selectedString === 'Database/Big Data') {
        return data;
    } 
} 

let userRole = localStorage.getItem('role');
let roleId = localStorage.getItem('roleId');

function selectSkill(selectedSkillElement) {
    document.querySelectorAll('.skill').forEach(skill => {
        skill.classList.remove('selected');
    });

    selectedSkillElement.classList.add('selected');
}

// Add event listeners to each skill
document.querySelectorAll('.skill').forEach(skill => {
    skill.addEventListener('click', function() {
        selectSkill(this);

        
    });
});
// Can not use Form to submit

document.getElementById('pdfUploader').addEventListener('change', (event)=> {
    let file = event.target.files[0];

    if (!file) {
        console.log("No file selected.");
        return;
    }

    // Check if the file is a PDF
    if (file.type !== "application/pdf") {
        console.log("Please select a PDF file.");
        return;
    }

    // Create FormData and append the file
    let formData = new FormData();
    formData.append("file", file, file.name);

    let stSuUrl = '/supervisorInfo/supervisor_upload_resume/';
    if (userRole === 'student') {
        stSuUrl = '/studentInfo/student_upload_resume/';
    }
    console.log(stSuUrl)
    let roleId = localStorage.getItem('roleId');
    // doFetch(stSuUrl + roleId, 'POST', formData);
    fetch('http://localhost:9998' + stSuUrl + roleId, {
        method: "POST",
        body: formData,
      })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
});


submit.addEventListener('click', (event) => {
    let selectedSkillvalue = document.querySelector('.skill.selected');
    if (selectedSkillvalue !== null) {
        selectedSkillvalue = selectedSkillvalue.textContent;
    } else {
        selectedSkillvalue = '';
    }
    let stSuUrl = '/profile/supervisor';
    if (userRole === 'student') {
        stSuUrl = '/studentInfo/student_update';
    }
    let quaOrStrength = "strength";
    let stOrSu = "student_id";
    if(role === 'supervisor') {
        quaOrStrength = "qualification";
        stOrSu = "supervisor_id"
    }
    doFetch(stSuUrl, 'PUT', {
        [stOrSu]: Number(roleId),
        "first_name": name1.value,
        "last_name": name2.value,
        "email": email.value,
        "skills": selectedSkillvalue,
        [quaOrStrength]: strengthInput.value,
    })
})

logout.addEventListener('click', ()=>{
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('roleId');
    localStorage.removeItem('username');
    localStorage.removeItem('password');
})
