document.addEventListener("DOMContentLoaded", function() {
    const canvas = document.getElementById('shipCanvas');
    const ctx = canvas.getContext('2d');
    const BASE_URL = "http://localhost:8000/ships/";
    let centralShipId = 1; // Установим начальное значение
    let ships = [];
    let scale = 1;



    async function getAllShips() {
        try {
            const response = await fetch(`${BASE_URL}`);
            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }
            ships = await response.json();
            console.log("Полученные данные всех кораблей:", ships);
        } catch (error) {
            console.error("Ошибка при получении данных кораблей:", error);
            ships = [];
        }
    }

    document.addEventListener("keydown", function(event) {
        const index = ships.findIndex(ship => ship.id === centralShipId);
        if (event.key === "ArrowUp" && index < ships.length - 1) {
            centralShipId = ships[index + 1].id;
        } else if (event.key === "ArrowDown" && index > 0) {
            centralShipId = ships[index - 1].id;
        }
        if (event.key === "+") {
            scale *= 2; // Увеличиваем масштаб
        } else if (event.key === "-") {
            scale /= 2; // Уменьшаем масштаб
        }
    });




    function drawShip(ship, centralShip) {
        // Вычисляем относительные координаты относительно центрального корабля
        const relativeX = canvas.width / 2 + (ship.x - centralShip.x) * scale;
        const relativeY = canvas.height / 2 + (ship.y - centralShip.y) * scale;
    
        // Проверяем, находится ли корабль в пределах холста
        if (relativeX + ship.width / 2 < 0 || relativeX - ship.width / 2 > canvas.width ||
            relativeY + ship.length / 2 < 0 || relativeY - ship.length / 2 > canvas.height) {
            return; // Если корабль за пределами холста, не отрисовываем его
        }
    
        ctx.save();
        ctx.translate(relativeX, relativeY);
        const canvasAngle = Math.PI / 2 - ship.direction * Math.PI / 180;
        ctx.rotate(canvasAngle);
    
        ctx.fillStyle = ship.id === centralShip.id ? 'red' : 'navy'; // Центральный корабль выделяем цветом
        ctx.fillRect(-ship.width / 2, -ship.length / 2, ship.width, ship.length);
    
        ctx.restore();
    }
    

    function drawText() {
        const centralShip = ships.find(ship => ship.id === centralShipId);
        if (centralShip) {
            const text = `ID: ${centralShip.id}, X: ${centralShip.x.toFixed(2)}, Y: ${centralShip.y.toFixed(2)}, Скорость: ${centralShip.speed}, Направление: ${centralShip.direction.toFixed(2)}`;
            ctx.fillStyle = 'black';
            ctx.font = '16px Arial';
            ctx.fillText(text, 10, 20);
        }
    }

    function update() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        const centralShip = ships.find(ship => ship.id === centralShipId);
        if (centralShip) {
            ships.forEach(ship => {
                drawShip(ship, centralShip);
            });
        }

        drawText(); // Обновляем текст
        requestAnimationFrame(update);
    }

    setInterval(getAllShips, 1000); // Запрашиваем данные всех кораблей каждую секунду
    update();
});
