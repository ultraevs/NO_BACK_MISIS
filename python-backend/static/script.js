const url = 'https://urbaton.ultraevs.ru/login/';


const button = document.querySelector(".button1");

async function getData() {

    let input_email = document.querySelector(".input-field-email").value;
    let input_password = document.querySelector(".input-field-password").value;

    const data = new URLSearchParams();
    data.append("email", input_email);
    data.append("password", input_password);

    const response = await fetch(url, {
        method: "POST",
        body: data,
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
    });

    const json = await response.json();
    console.log("Успех:", JSON.stringify(json));
    if (json.data == "ACCEPT") {
        window.location = "https://urbaton.ultraevs.ru/profile/";
    }
    else if (json.data == "Нет такого юзера") {
        alert("Нет такого юзера")
    }
    else if (json.data == "Неверный пароль") {
        alert("Неверный пароль")
    }


}

button.addEventListener('click', getData)


const url_r = 'https://urbaton.ultraevs.ru/register/';

const button_r = document.querySelector(".button2");

async function postData() {

    let input_email = document.querySelector(".input-field-email").value;
    let input_password = document.querySelector(".input-field-password").value;
    let input_name = document.querySelector(".input-field-name").value;

    const data = new URLSearchParams();
    data.append("email", input_email);
    data.append("password", input_password)
    data.append("name", input_name)

    const response = await fetch(url_r, {
        method: "POST",
        body: data,
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
    });

    const json = await response.json();
    console.log("Успех:", JSON.stringify(json));
    if (json.data == "ACCEPT") {
        window.location = "https://urbaton.ultraevs.ru/profile";
    }
    else if (json.data == "Нет такого юзера") {
        alert("Нет такого юзера")
    }
    else if (json.data == "Неверный пароль") {
        alert("Неверный пароль")
    }

}

button_r.addEventListener('click', postData)

const url_f = 'https://urbaton.ultraevs.ru/forgot/';

const button_f = document.querySelector(".button4");

async function forgot() {

    let input_email = document.querySelector(".input-field-email").value;

    const data = new URLSearchParams();
    data.append("email", input_email);

    const response = await fetch(url_f, {
        method: "POST",
        body: data,
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
    });
    
    const json = await response.json();
    console.log("Успех:", JSON.stringify(json));
    if (json.data == "Письмо Отправлено") {
        alert("Письмо отправлено")
        window.location = "https://urbaton.ultraevs.ru/profile";
    }


}

button_f.addEventListener('click', forgot)
