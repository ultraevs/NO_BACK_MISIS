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

ymaps.ready(init);

let Moscow = [55.7522, 37.6156];

const parkingDots = [
    {
        lat: 55.7364,
        lon: 37.6535,
        name: "Парковка на районе",
        price: 200,
        parking: {
            1: "занято",
            2: "занято",
            3: "свободно",
            4: "занято",
            5: "свободно",
        },
    },
    {
        lat: 55.7419,
        lon: 37.6098,
        name: "Парковка у лофта",
        price: 300,
        parking: {
            1: "свободно",
            2: "занято",
            3: "свободно",
            4: "занято",
            5: "занято",
        },
    },
    {
        lat: 55.7429,
        lon: 37.6560,
        name: "Парковка у зала",
        price: 250,
        parking: {
            1: "занято",
            2: "занято",
            3: "занято",
            4: "занято",
            5: "свободно",
        },
    },
]

console.log(parkingDots.length);

const text = document.getElementById("text");

function init() {

    const map = new ymaps.Map("map", {
        center: Moscow,
        zoom: 12,
    });

    map.controls.remove("searchControl");
    map.controls.remove("trafficControl");
    map.controls.remove("fullscreenControl");
    map.controls.remove("zoomControl")
    map.controls.remove("typeSelector");
    map.controls.remove("rulerControl");
    map.controls.remove("scrollZoom");

    for (let i = 0; i < parkingDots.length; i++) {
        console.log(parkingDots[i].name);
        let placemark = new ymaps.Placemark([parkingDots[i].lat, parkingDots[i].lon], {
            hintContent: parkingDots[i].name,
        },
            {
                iconLayout: "default#image",
                iconImageHref: "https://cdn-icons-png.flaticon.com/128/1783/1783356.png",
                iconImageSize: [25, 25],
                iconImageOffset: [0, 0],
            });

        placemark.events.add("click", function () {
            bottom.classList.toggle("active");
            console.log(text.innerHTML);
            if (text.innerHTML === "Some text") {
                text.innerHTML = parkingDots[i].name;
            } else {
                text.innerHTML = "Some text";
            }

            if (arrow.classList.contains("bx-up-arrow")) {
                arrow.classList.remove("bx-up-arrow");
                arrow.classList.add("bx-down-arrow");
            } else {
                arrow.classList.remove("bx-down-arrow");
                arrow.classList.add("bx-up-arrow");
            }

            const bottom__array = document.createElement("div");
            bottom__array.classList.add("bottom__text");

            const historyTitle = document.createElement("p");
            historyTitle.appendChild(document.createTextNode("jbduibowro"))
            bottom__array.appendChild(historyTitle);

            bottom.appendChild(bottom__array);

        })

        map.geoObjects.add(placemark);
    }

    console.log(map.geoObjects);
}

const bottom = document.querySelector(".search__bottom");
const arrow = document.querySelector(".bottom__arrow i");

// arrow.addEventListener("click", function () {
//     if (arrow.classList.contains("bx-up-arrow")) {
//         arrow.classList.remove("bx-up-arrow");
//         arrow.classList.add("bx-down-arrow");
//     } else {
//         arrow.classList.remove("bx-down-arrow");
//         arrow.classList.add("bx-up-arrow");
//     }

//     bottom.classList.toggle("active");
// })

const numOfAvailable = document.querySelector(".numOfAvailable");
const wordOfAvailable = document(".wordOfAvailable");

function numAndWord() {
    numOfAvailable.innerHTML = parkingDots.length;
    console.log(typeof numOfAvailable.innerHTML)
}

numAndWord();