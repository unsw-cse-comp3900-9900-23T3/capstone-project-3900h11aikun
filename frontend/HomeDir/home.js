import { doFetch, cutStringBeforeSpace } from "../helper.js";

const home = document.getElementById('home');
const myPro = document.getElementById('mypro');
const apply = document.getElementById('apply');
const profile = document.getElementById('profile');
const logout = document.getElementById('logout');
const all = document.getElementById('all');
const recommand = document.getElementById('recommand');
const projects = document.getElementById('projects');
let userRole = localStorage.getItem('role');
if (userRole === 'partner') {
    recommand.value = 'Post a project'
}
// Interaction display
function naviDisplay (item) {
    item.addEventListener('mouseover', (event) => {
        item.style.color = `rgb(${0}, ${193}, ${193})`;
    });
    item.addEventListener('mouseleave', (event) => {
        item.style.color = 'white';
    });
};

function optDisplay (item) {
    item.addEventListener('mouseover', (event) => {
        item.style.borderColor = `rgb(${0}, ${193}, ${193})`;
    });
    item.addEventListener('mouseleave', (event) => {
        item.style.borderColor = `rgb(${232}, ${235}, ${238})`;
    });
};

recommand.addEventListener('click', (event) => {
    recommand.style.background = `rgb(${0}, ${193}, ${193})`;
    all.style.background = `rgb(${232}, ${235}, ${238})`;
    if (userRole === 'partner') {
        alert('post project have not implemented');
    } else {
        showAllOrRecomandProjects(false);
    }
});

all.addEventListener('click', (event) => {
    all.style.background = `rgb(${0}, ${193}, ${193})`;
    recommand.style.background = `rgb(${232}, ${235}, ${238})`;
    showAllOrRecomandProjects(true);
});
naviDisplay(home);
naviDisplay(myPro);
naviDisplay(apply);
naviDisplay(profile);
naviDisplay(logout);
optDisplay(all);
optDisplay(recommand);


// Example of post a project
function newPro (projectName, projectRequirements) {
    const project = document.createElement('div');
    project.style.width = '370px';
    project.style.height = '130px';
    project.style.background = 'white';
    project.style.margin = '10px';
    project.style.borderRadius = '20px';

    const name = document.createElement('div');
    name.textContent = projectName;
    name.style.width = '350px';
    name.style.height = '30px';
    name.style.marginLeft = '10px';
    name.style.marginTop = '10px';
    name.style.fontSize = '1.2em';
    name.style.fontWeight = 'bold';

    project.appendChild(name);

    const require = document.createElement('div');
    require.textContent = projectRequirements;
    require.style.width = '350px';
    require.style.height = '30px';
    require.style.marginLeft = '10px';
    require.style.marginTop = '10px';
    require.style.fontSize = '1em';

    project.appendChild(require);

    const more = document.createElement('input');
    more.type = 'button';
    more.value = 'View More';
    more.style.height = '30px';
    more.style.width = '150px';
    more.style.border = '0px';
    more.style.marginLeft = '110px';
    more.style.marginTop = '10px';
    more.style.borderRadius = '10px';
    more.style.background = `rgb(${232}, ${235}, ${238})`;
    more.addEventListener('mouseover', (event) => {
        more.style.background = `rgb(${0}, ${193}, ${193})`;
        more.style.color = 'white';
    });
    more.addEventListener('mouseleave', (event) => {
        more.style.background = `rgb(${232}, ${235}, ${238})`;
        more.style.color = 'black';
    });

    project.appendChild(more);

    projects.appendChild(project);
}

newPro('Project Name', 'Project re');
function showAllOrRecomandProjects(isAll) {
    let url = '/profile/project';
    if (!isAll) {
        projects.textContent = '';
        alert('change thiis url when backend is ready!!!');
        url = 'change thiis!!!';
    }
    doFetch(url, 'GET').then((projects)=>{
        console.log(projects);
        projects.forEach(project => {
            let descriptionString = project.description;
            if (descriptionString.length > 80) {
                descriptionString = cutStringBeforeSpace(descriptionString, 80) + ' ...';
            } 
            newPro(project.title, descriptionString);
        });
    })
}
showAllOrRecomandProjects(true);

logout.addEventListener('click', ()=>{
    localStorage.removeItem('token');
    localStorage.removeItem('role');
})