let availableKeywords = [
    "Ельцин Центр",
    "Высоцкий",
    "Отель",
    "Парк Маяковского",
    "ТРЦ Гринвич",
    "Парк Зеленая роща",
];

const resultBox = document.querySelector(".box__result");
const inputBox = document.getElementById("input-box");

inputBox.onkeyup = function () {
    let result = [];
    let input = inputBox.value;
    if (input.length) {
        result = availableKeywords.filter((keyword) => {
            return keyword.toLowerCase().includes(input.toLowerCase());
        });

        // console.log(result);
    }

    display(result);

    if (!result.length) {
        resultBox.innerHTML = "";
    }
}

function display(result) {
    const content = result.map((list) => {
        return "<li onclick=selectInput(this)>" + list + "</li>";
    });

    resultBox.innerHTML = "<ul>" + content.join("") + "</ul>";
}

function selectInput(list) {
    inputBox.value = list.innerHTML;
    resultBox.innerHTML = "";
}

async function getData3(url, data = {}) {
    const response = await fetch(url, {
        method: "GET",
        mode: "cors",
        cache: "no-cache",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
        },
        redirect: "follow",
        referrerPolicy: "no-referrer",
    });
    return await response.json();
}

getData3("https://urbaton.ultraevs.ru/name/", { answer: 42 }).then((data) => {
    document.querySelector('.back_name').innerHTML = data.name;

})
