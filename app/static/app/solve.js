// представление исходного решения в более удобный вид
var solveString = document.getElementById("solve-string");

var sides = JSON.parse(document.getElementById("sides").innerHTML);

var solveArray = solveString.innerHTML.split(" ");

var russianColors = {
    "yellow": "желтую",
    "red": "красную",
    "green": "зеленую",
    "white": "белую",
    "orange": "оранжевую",
    "blue": "синюю"
};


var ol = document.createElement("ol");
for (let move of solveArray) {
    let li = document.createElement("li");

    let side = move[0];

    if (move[1] === "'") {
        li.innerHTML = "Поверните <b>" + russianColors[sides[side]] +"</b> сторону <b>против</b> часовой стрелки"
    } else if (move[1] === "2") {
        li.innerHTML = "Поверните <b>" + russianColors[sides[side]] +"</b> сторону <b>дважды по</b> часовой стрелке"
    } else {
        li.innerHTML = "Поверните <b>" + russianColors[sides[side]] +"</b> сторону <b>по</b> часовой стрелке"
    }

    ol.appendChild(li)
}

document.getElementById("solve").appendChild(ol);