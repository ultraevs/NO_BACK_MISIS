const button = document.querySelector("button")

async function back(){
    window.location = "/static/pages/main/index.html";
}

button.addEventListener('click', back)