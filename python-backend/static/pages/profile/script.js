async function getData1(url, data = {}) {
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

let dataEx;
getData1("https://urbaton.ultraevs.ru/history/", { answer: 42 }).then((data) => {
    console.log(data);
    const ul = document.getElementById("list");
    for (let i = 0; i < data.length; i++) {
        const block = document.createElement("div");
        block.classList.add("layer__block");

        const block__left = document.createElement("div");
        block__left.classList.add("block__left");
        const block__right = document.createElement("div");
        block__right.classList.add("block__right");

        const number = document.createElement("p");
        const name = document.createElement("p");
        const carNumber = document.createElement("p");

        number.appendChild(document.createTextNode(data[i].id));
        name.appendChild(document.createTextNode(data[i].name));
        carNumber.appendChild(document.createTextNode(data[i].number));

        block__left.appendChild(number);
        block__left.appendChild(name);
        block__left.appendChild(carNumber);

        const date = document.createElement("p");
        const icon = document.createElement("i");

        date.appendChild(document.createTextNode(data[i].datee));
        icon.classList.add("bx")
        icon.classList.add("bx-info-circle")

        block__right.appendChild(date);
        block__right.appendChild(icon);

        block.appendChild(block__left);
        block.appendChild(block__right);

        ul.appendChild(block);
    }
});

async function getData2(url, data = {}) {
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

getData2("https://urbaton.ultraevs.ru/tests/", { answer: 42 }).then((data) => {
    document.querySelector('.money').innerHTML = data.count;

})
const answer = document.getElementById("value-2")

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
