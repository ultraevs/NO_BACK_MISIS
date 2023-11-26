// Главный объект информации
const parkingDots = [
    {
        lat: 55.7364,
        lon: 37.6535,
        name: "Парковка на районе",
        adress: "Ул. Малые Каменщики",
        price: 200,
        parking: {
            1: "занято",
            2: "занято",
            3: "свободно",
            4: "занято",
            5: "свободно",
            6: "свободно",
            7: "свободно",
            8: "свободно",
            9: "занято",
            10: "свободно",
            11: "занято",
            12: "свободно",
        },
    },
    {
        lat: 55.7419,
        lon: 37.6098,
        name: "Парковка у лофта",
        adress: "Ул. Новодмитровская",
        price: 300,
        parking: {
            1: "свободно",
            2: "занято",
            3: "свободно",
            4: "занято",
            5: "свободно",
            6: "занято",
            7: "свободно",
            8: "занято",
            9: "свободно",
            10: "занято",
            11: "свободно",
            12: "занято",
        },
    },
    {
        lat: 55.7429,
        lon: 37.6560,
        name: "Парковка у зала",
        adress: "Ул. Таганская",
        price: 250,
        parking: {
            1: "занято",
            2: "занято",
            3: "занято",
            4: "занято",
            5: "свободно",
            6: "занято",
            7: "занято",
            8: "занято",
            9: "занято",
            10: "свободно",
            11: "свободно",
            12: "занято",
            13: "занято",
            14: "занято",
            15: "занято",
            16: "занято",
            17: "свободно",
            18: "занято",
            19: "занято",
            20: "занято",
            21: "занято",
            22: "свободно",
            23: "свободно",
            24: "занято",
        },
    },
    {
        lat: 55.7559,
        lon: 37.6098,
        name: "Парковка у музея МГУ",
        adress: "Ул. Малые Каменщики",
        price: 400,
        parking: {
            1: "занято",
            2: "занято",
            3: "занято",
            4: "занято",
            5: "свободно",
            6: "занято",
            7: "занято",
            8: "занято",
            9: "занято",
            10: "свободно",
            11: "свободно",
            12: "занято",
        },
    },
]

// Создание массива с названиями всех парковок
let availableKeywords = [];

for (let i = 0; i < parkingDots.length; i++) {
    availableKeywords.push(parkingDots[i].name)
};

// Переменные для краткой инфы о парковке
const parkingTitle = document.querySelector(".active__title");
const parkingAdress = document.querySelector(".active__adress");
const parkingPlaces = document.querySelector(".active__places");
const bottomActive = document.querySelector(".bottom__active");
const bottomBtn = document.querySelector(".bottom__btn");

// Наложение функции открытия окна бронирования
bottomBtn.addEventListener("click", toOpenOrCloseBookingSection)

// Переменные для поиска
const bottom = document.querySelector(".search__bottom");
const resultBox = document.querySelector(".box__result");
const inputBox = document.getElementById("input-box");

// Переменные для окна бронирования
const booking = document.querySelector(".booking");
const bookingTitle = document.querySelector(".booking__title");
const bookingAdress = document.querySelector(".booking__adress");
const searchBtn = document.querySelector(".search__btn");
const bookingPlaces = document.querySelector(".booking__places");
const placesLeft = document.querySelector(".places__left");
const placesRight = document.querySelector(".places__right");

// Переменные, показывающие данные о свободных местах и загруженности парковок
const numOfAvailable = document.querySelector(".numOfAvailable");
const wordOfAvailable = document.querySelector(".wordOfAvailable");
const load = document.querySelector(".load");

// Переменные для окна с оплатой
const pay = document.querySelector(".pay");
const bookingBtn = document.querySelector(".booking__btn");
bookingBtn.addEventListener("click", function () {
    pay.classList.toggle("active");
})

const topBtn = document.querySelector(".pay__top__icon");
topBtn.addEventListener("click", function () {
    pay.classList.toggle("active");
})

// Объявление функции, которая транслирует данные о парковках
numAndWord();

// Наложение функции закрытия окна бронирования при нажатии на иконку
const bookingCloseBtn = document.querySelector(".top__icon");
bookingCloseBtn.addEventListener("click", toOpenOrCloseBookingSection)

// Функция, при которой реализуется закрытие окна бронирования
function toOpenOrCloseBookingSection() {
    booking.classList.toggle("active");
}

// Блок кода для реализации поиска
inputBox.onkeyup = function () {
    let result = [];
    let input = inputBox.value;
    if (input.length) {
        result = availableKeywords.filter((keyword) => {
            return keyword.toLowerCase().includes(input.toLowerCase());
        });
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
// Конец блока с кодом, отвечающего за поиск

// Функция присваивания класса "active"
function toggleClassActive() {
    bottom.classList.toggle("active");
    bottomActive.classList.toggle("active");
    bottomBtn.classList.toggle("active");
}

// Функционал загружающий всю инфу о паркове как и краткая инфа, так и инфа с бронированием
searchBtn.addEventListener("click", function () {

    toggleClassActive();

    for (let i = 0; i < parkingDots.length; i++) {
        if (inputBox.value === parkingDots[i].name) {
            parkingTitle.innerHTML = parkingDots[i].name;
            parkingAdress.innerHTML = parkingDots[i].adress;

            let count = 0;
            for (key in parkingDots[i].parking) {
                count++;
            }

            parkingPlaces.innerHTML = count;

            bookingTitle.innerHTML = parkingDots[i].name;
            bookingAdress.innerHTML = parkingDots[i].adress;

            let k = 0;
            for (key in parkingDots[i].parking) {
                k++;
                const bookingPlace = document.createElement("div");
                bookingPlace.classList.add("booking__place");

                const placeNum = document.createElement("div");
                placeNum.classList.add("placeNum");
                placeNum.appendChild(document.createTextNode(String(k)));

                const border = document.createElement("div");
                border.classList.add("between");

                const placeStatus = document.createElement("div");
                placeStatus.classList.add("placeStatus");
                if (parkingDots[i].parking[key] === "занято") {
                    bookingPlace.classList.add("ocupated");
                } else {
                    bookingPlace.classList.add("free");
                    bookingPlace.addEventListener("click", function () {
                        bookingPlace.classList.toggle("active");
                    })
                }
                placeStatus.appendChild(document.createTextNode(parkingDots[i].parking[key]));

                bookingPlace.appendChild(placeNum);
                bookingPlace.appendChild(placeStatus);

                if (k <= (count / 2)) {
                    placesLeft.appendChild(border);
                    placesLeft.appendChild(bookingPlace);
                } else {
                    placesRight.appendChild(border);
                    placesRight.appendChild(bookingPlace);
                }
            }
        }
    }
})

// Запуск работы карт
ymaps.ready(init);

// Координаты центра карты
let Moscow = [55.7522, 37.6156];

// Функция для работы с картой
function init() {
    // Объявление карты
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

    // Создание точек
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
            toggleClassActive();

            parkingTitle.innerHTML = parkingDots[i].name;
            parkingAdress.innerHTML = parkingDots[i].adress;

            let count = 0;
            for (key in parkingDots[i].parking) {
                count++;
            }

            parkingPlaces.innerHTML = count;

            bookingTitle.innerHTML = parkingDots[i].name;
            bookingAdress.innerHTML = parkingDots[i].adress;

            let k = 0;
            for (key in parkingDots[i].parking) {
                k++;
                const bookingPlace = document.createElement("div");
                bookingPlace.classList.add("booking__place");

                const placeNum = document.createElement("div");
                placeNum.classList.add("placeNum");
                placeNum.appendChild(document.createTextNode(String(k)));

                const border = document.createElement("div");
                border.classList.add("between");

                const placeStatus = document.createElement("div");
                placeStatus.classList.add("placeStatus");
                if (parkingDots[i].parking[key] === "занято") {
                    bookingPlace.classList.add("ocupated");
                } else {
                    bookingPlace.classList.add("free");
                    bookingPlace.addEventListener("click", function () {
                        bookingPlace.classList.toggle("active");
                        console.log("HI");
                    })
                }
                placeStatus.appendChild(document.createTextNode(parkingDots[i].parking[key])); //статус

                bookingPlace.appendChild(placeNum);
                bookingPlace.appendChild(placeStatus);

                if (k <= (count / 2)) {
                    placesLeft.appendChild(border);
                    placesLeft.appendChild(bookingPlace);
                } else {
                    placesRight.appendChild(border);
                    placesRight.appendChild(bookingPlace);
                }
            }
        })

        map.geoObjects.add(placemark);
    }

    console.log(map.geoObjects);
}

function numAndWord() {
    let len = parkingDots.length;
    numOfAvailable.innerHTML = len;
    let numm = numOfAvailable.innerHTML;
    let need = numm[numm.length - 1];
    if (need === "1") {
        wordOfAvailable.innerHTML = "парковка";
    } else if (need <= "4") {
        wordOfAvailable.innerHTML = "парковки";
    } else {
        wordOfAvailable.innerHTML = "парковок";
    }

    if (len <= 10) {
        load.innerHTML = "Низкая";
    } else if (len <= 25) {
        load.innerHTML = "Средняя";
    } else {
        load.innerHTML = "Высокая";
    }
}