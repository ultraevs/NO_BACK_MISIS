const button = document.querySelector("button")

async function back(){
    window.location = "/static/pages/main/index.html";
}

button.addEventListener('click', back)

const answer = document.getElementById("value-2")
const url = 'https://urbaton.ultraevs.ru/commit-test/'

async function postData() {
    await fetch(url, {
        method: "POST",
        body: {},
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
    });
}

answer.addEventListener('click', postData)
