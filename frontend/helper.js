export function doFetch(url, method, body) {
    console.log(body)
    const headers = {};
    const options = {};
    if (body) {
        headers["Content-Type"]= 'application/json; charset=UTF-8';
        options.body = JSON.stringify(body); 
    }

    if (localStorage.getItem("token")) {
        headers.Authorization = localStorage.getItem("token");
    }

    options.headers = headers;
    options.method = method;
    
    return fetch('http://localhost:9998' + url, options).then(resp =>{
        
        return resp.json();
    })
}

export function cutStringBeforeSpace(str, length){
    let finalString = str.substring(0, length);
    let lastSpaceIndex = finalString.lastIndexOf(' ');
    return finalString.substring(0, lastSpaceIndex);

}

export function uploadPdf(uploader, url, method, errorField) {
    uploader.addEventListener('change', (event)=> {
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
        console.log('pppp')
        // doFetch(stSuUrl + roleId, 'POST', formData);
        fetch('http://localhost:9998' + url, {
            method: method,
            body: formData,
          })
        .then(response => response.json())
        .then(data => {
            console.log(errorField)
            errorField.classList.remove("hide")
            errorField.textContent = "Upload successfully";
        })
        .catch(error => {
            errorField.classList.remove("hide")
            errorField.textContent = "Upload failed"
        });
    });
}