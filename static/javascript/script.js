// Initialize map
const map = L.map('map').setView([10.7769, 106.6670], 15);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

const geocoder = L.Control.Geocoder.nominatim();

function addMarker(lat, lng, popupText) {
    marker = L.marker([lat, lng]).addTo(map)
        .bindPopup(popupText)
        .openPopup();
    map.setView([lat, lng], 18);
    return marker;
}

let routeLine;
function drawRoute(route) {
    if (routeLine) map.removeLayer(routeLine);
    routeLine = L.polyline(route, { color: 'blue' }).addTo(map);
    map.fitBounds(routeLine.getBounds());
}

let routeLines = [];

function getRandomColor() {
    // Tạo các giá trị ngẫu nhiên cho màu đỏ, xanh lá, xanh dương và độ trong suốt
    const r = Math.floor(Math.random() * 256);
    const g = Math.floor(Math.random() * 256);
    const b = Math.floor(Math.random() * 256);
    const opacity = 0.5;

    // Trả về màu ở định dạng rgba
    return `rgba(${r}, ${g}, ${b}, ${opacity})`;
}

function drawRoutes(routes) {
    // Xóa các tuyến đường cũ
    routeLines.forEach(line => map.removeLayer(line));
    routeLines = [];

    // Vẽ từng tuyến đường với màu, flow, và độ rộng riêng
    routes.forEach(routeData => {
        const route = routeData.route;
        const flow = routeData.flow;
        const color = getRandomColor();

        // Tạo tuyến đường với độ rộng lớn hơn (ví dụ: 8)
        const routeLine = L.polyline(route, { color: color, weight: 8 }).addTo(map);
        routeLines.push(routeLine);

        // Thêm popup để hiển thị flow trên tuyến đường
        routeLine.bindPopup(`Flow: ${flow}`).openPopup();

        // Thêm bindTooltip để hiển thị flow trên tuyến đường
        routeLine.bindTooltip(`Flow: ${flow}`, { permanent: true, direction: "center", className: "flow-tooltip" }).openTooltip();
    });

    // Điều chỉnh phạm vi bản đồ để phù hợp với tất cả các tuyến đường
    const bounds = L.latLngBounds(routeLines.flatMap(line => line.getLatLngs()));
    map.fitBounds(bounds);
}

async function findRoute(startCoords, endCoords, algorithm) {
    try {
        const response = await fetch('/find_route', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ start: startCoords, end: endCoords, algorithm })
        });
        const result = await response.json();
        result.routes ? drawRoutes(result.routes) : alert("Could not find any routes.");
    } catch (error) {
        console.error('Error:', error);
    }
}

let startMarker = null;
let endMarker = null;
let tempMarker = null;

function handleSearch(inputId, resultDivId, labelText, coordVar, startflag, endflag) {
    const searchValue = document.getElementById(inputId).value;
    const resultsDiv = document.getElementById(resultDivId);
    resultsDiv.innerHTML = '';

    if (!searchValue) return;

    geocoder.geocode(searchValue, function(results) {
        if (results && results.length > 0) {
            results.slice(0, 3).forEach(result => {
                const resultItem = document.createElement('div');
                resultItem.className = 'result-item p-2 border border-gray-300 mb-1 cursor-pointer';
                resultItem.textContent = result.name;
                resultItem.dataset.lat = result.center.lat;
                resultItem.dataset.lng = result.center.lng;

                resultItem.addEventListener('mouseover', function() {
                    tempMarker = addMarker(this.dataset.lat, this.dataset.lng, `${labelText}`)
                });

                resultItem.addEventListener('mouseout', function() {
                    if (tempMarker) map.removeLayer(tempMarker);
                    tempMarker = null;
                });

                resultItem.addEventListener('click', function() {
                    document.getElementById(inputId).value = this.textContent;
                    window[coordVar] = [this.dataset.lat, this.dataset.lng];
                    if (startflag){
                        if (startMarker) map.removeLayer(startMarker);
                        startMarker = tempMarker;
                    }
                    else if (endflag){
                        if (endMarker) map.removeLayer(endMarker);
                        endMarker = tempMarker;
                    }
                    resultsDiv.innerHTML = '';
                });

                resultsDiv.appendChild(resultItem);
            });
        } else {
            alert(`${labelText} location not found.`);
        }
    });
}

document.getElementById("search-start").addEventListener("click", () => handleSearch("start", "result-start", "Starting point", "startCoords", true, false));
document.getElementById("search-end").addEventListener("click", () => handleSearch("end", "result-end", "Ending point", "endCoords", false, true));

document.getElementById("search-form").addEventListener("submit", function(event) {
    event.preventDefault();
    if (typeof startCoords == 'undefined' || typeof endCoords == 'undefined') {
        alert("Vui lòng nhập đầy đủ điểm đi và điểm đến.");
        return;
    }
    const algorithm = document.getElementById("algorithm").value;
    findRoute(startCoords, endCoords, algorithm);
});
