var colors = ["grey", 'yellow', 'white', "green", "red", "blue", "orange"];

var colorsRGB = {
    "rgb(128, 128, 128)": 'grey',
    "rgb(255, 255, 0)": 'yellow',
    "rgb(0, 128, 0)": "green",
    "rgb(255, 255, 255)": "white",
    "rgb(255, 0, 0)": "red",
    "rgb(255, 165, 0)": "orange",
    "rgb(0, 0, 255)": "blue"
};

function changeColor(block) {
    var currentColor = colorsRGB[getComputedStyle(block).backgroundColor];
    if (currentColor == colors[colors.length - 1]) {
        block.style.backgroundColor = colors[0];
    } else {
        block.style.backgroundColor = colors[colors.indexOf(currentColor) + 1];
    }
}

// генерирует случайный кубик
function randomFilling() {
    var sides = "URFDLB";

    var sidesColors = {
        "U": colors[1],
        "R": colors[4],
        "F": colors[3],
        "D": colors[2],
        "L": colors[6],
        "B": colors[5]
    };

    var cube = {};

    // генерация "решенного" куба
    for (let i=0; i<6; i++) {
        for (let j=1; j<10; j++) {
            cube[sides[i]+j] = sides[i]
        }
    }

    var combinations = ["U", "U'", "U2", "R", "R'", "R2", "F", "F'", "F2", "D", "D'", "D2", "L", "L'", "L2", "B", "B'", "B2"];

    var myCombinations = [];

    // наполнение массива с комбинациями
    for (let i=0; i<30; i++) {
        myCombinations.push(combinations[Math.floor(Math.random()*combinations.length)]);
    }

    // кручение-верчение
    for (let move of myCombinations) {
        makePermutation(move);
    }

    var emptyBlocks = document.getElementsByClassName("block");

    // очищает кубик
    for (let i = 0; i < emptyBlocks.length; i++) {
        emptyBlocks[i].style.backgroundColor = colors[0]
    }

    // заполнение куба
    cubeFilling();

    // функция для перемещения граней куба, принимает комбинацию, согласно которой должно совершаться перемещение
    function makePermutation(move) {
        let bufferCube = Object.assign({}, cube);

        // функция, осуществляющая изменения в основном кубе
        function moveBlock(from, to) {
            for (let j=0; j<3; j++) {
                bufferCube[to[3]+to[j]] = cube[from[3]+from[j]]
            }
        }

        // константы для перестановки "лица"
        let face = move[0];

        let face123 = "123" + face;
        let face369 = "369" + face;
        let face987 = "987" + face;
        let face741 = "741" + face;


        let movement;
        if (move[0] == "U") {
            movement = "123F123L123B123R123F"
        } else if (move[0] == "L") {
            movement = "147F147D963B147U147F"
        } else if (move[0] == "F") {
            movement = "369L987U741R123D369L"
        } else if (move[0] == "R") {
            movement = "369F369U741B369D369F"
        } else if (move[0] == "B") {
            movement = "147L789D963R321U147L"
        } else {
            movement = "789F789R789B789L789F"
        }

        if (move[1]) {
            if (move[1] == "'") {
                let newMovement = '';
                for (let i=movement.length-1; i>0; i-=4) {
                    newMovement += movement.slice(i-3, i+1)
                }
                movement = newMovement;

                moveBlock(face123, face741);
                moveBlock(face741, face987);
                moveBlock(face987, face369);
                moveBlock(face369, face123)
            } else {
                movement = movement.slice(0, 4) + movement.slice(8, 12) + movement.slice(4, 8) + movement.slice(12, 16)

                moveBlock(face123, face987);
                moveBlock(face369, face741);
                moveBlock(face987, face123);
                moveBlock(face741, face369)
            }
        } else {
            moveBlock(face123, face369);
            moveBlock(face369, face987);
            moveBlock(face987, face741);
            moveBlock(face741, face123)
        }

        // если move[1] != "2"
        if (movement.length > 16) {
            let buffer;
            for (let i=0; i<movement.length-4; i+=4) {
                let from = buffer || movement.slice(0, i+4);
                let to = movement.slice(i+4, i+8);
                buffer = to;

                moveBlock(from, to)
            }
        } else {
            let from1 = movement.slice(0, 4);
            let to1 = movement.slice(4, 8);
            let from2 = movement.slice(8, 12);
            let to2 = movement.slice(12, 16);

            moveBlock(from1, to1);
            moveBlock(to1, from1);
            moveBlock(from2, to2);
            moveBlock(to2, from2);
        }

        cube = bufferCube;
    }

    // заполнение грани, принимает грань и строковое представление цветов для нее
    function faceFilling(face, str) {
        let blocks = face.getElementsByClassName("block");
        for (let i=0; i<9; i++) {
            blocks[i].style.backgroundColor = sidesColors[str[i]]
        }
    }

    function cubeFilling() {
        let faces = document.getElementsByClassName("cube-face");

        var cubeStringView = cubeToStringView();

        faceFilling(faces[0], cubeStringView.slice(0, 9));
        faceFilling(faces[3], cubeStringView.slice(9, 18));
        faceFilling(faces[2], cubeStringView.slice(18, 27));
        faceFilling(faces[5], cubeStringView.slice(27, 36));
        faceFilling(faces[1], cubeStringView.slice(36, 45));
        faceFilling(faces[4], cubeStringView.slice(45, 54))
    }

    // перевод полученного куба в стандартный вид для отладки.
    function cubeToStringView() {
        let str = "";

        for (let key in cube) {
            str += cube[key]
        }

        return str
    }
}

function findSolution() {
    // проверяет на ошибки
    function checkForErrors() {
        return true
    }

    if (checkForErrors()) {
        var blocks = document.getElementsByClassName("block");

        // определяет цветов сторон
        var constants = {};
        constants[getComputedStyle(blocks[4]).backgroundColor] = "U";
        constants[getComputedStyle(blocks[31]).backgroundColor] = "R";
        constants[getComputedStyle(blocks[22]).backgroundColor] = "F";
        constants[getComputedStyle(blocks[49]).backgroundColor] = "D";
        constants[getComputedStyle(blocks[13]).backgroundColor] = "L";
        constants[getComputedStyle(blocks[40]).backgroundColor] = "B";

        function parseBlock() {
            var cube = "";

            function parseSide(start, end) {
                var side = "";
                for (let i=start; i<end; i++) {
                    side += constants[getComputedStyle(blocks[i]).backgroundColor]
                }
                return side
            }

            cube += parseSide(0, 9);
            cube += parseSide(27, 36);
            cube += parseSide(18, 27);
            cube += parseSide(45, 54);
            cube += parseSide(9, 18);
            cube += parseSide(36, 45);

            return cube;
        }

        var cubeString = parseBlock();

        // перевод цветов в constants из RGB в строчный вид
        var sides = {};

        for (let color in constants) {
            sides[constants[color]] = colorsRGB[color]
        }

        var cubeData = {
            'cube': cubeString,
            'sides': sides
        };

        // сформировать в json строковое представление куба и цвета его сторон
        var cubeDataJSON = JSON.stringify(cubeData);

        var cubeStringInput = document.getElementById("cubeStringInput");
        cubeStringInput.setAttribute("value", cubeDataJSON);

    }
}