export function doFetch(url, method, body) {
    
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