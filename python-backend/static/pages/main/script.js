let availableKeywords = [
    "Курский вокзал",
    "НИТУ МИСИС",
    "Метро Таганская",
    "Ул. Земляной Вал",
    "Ул. Каменщики М.",
    "Пр-т Гагарина",
    "13ая Городская Больница",
    "Парковка МГУ",
    "Сокольники",
    "Парк Горького",
    "Метро Люблино",
    "Парковка МЭИ"
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