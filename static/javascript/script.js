// Initialize map
const map = L.map('map').setView([10.7769, 106.6670], 15);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

const geocoder = L.Control.Geocoder.nominatim();

function addMarker(lat, lng, popupText) {
    L.marker([lat, lng]).addTo(map)
        .bindPopup(popupText)
        .openPopup();
    map.setView([lat, lng], 18);
}

let routeLine;
function drawRoute(route) {
    if (routeLine) map.removeLayer(routeLine);
    routeLine = L.polyline(route, { color: 'blue' }).addTo(map);
    map.fitBounds(routeLine.getBounds());
}

async function findRoute(startCoords, endCoords, algorithm) {
    try {
        const response = await fetch('/find_route', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ start: startCoords, end: endCoords, algorithm })
        });
        const result = await response.json();
        result.route ? drawRoute(result.route) : alert("Could not find a route.");
    } catch (error) {
        console.error('Error:', error);
    }
}

function handleSearch(inputId, resultDivId, labelText, coordVar) {
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
                    tempMarker = L.marker([this.dataset.lat, this.dataset.lng])
                        .addTo(map)
                        .bindPopup(`${labelText}: ${this.textContent}`)
                        .openPopup();
                    map.setView([this.dataset.lat, this.dataset.lng], 18);
                });

                resultItem.addEventListener('mouseout', function() {
                    if (tempMarker) map.removeLayer(tempMarker);
                    tempMarker = null;
                });

                resultItem.addEventListener('click', function() {
                    document.getElementById(inputId).value = this.textContent;
                    window[coordVar] = [this.dataset.lat, this.dataset.lng];
                    addMarker(this.dataset.lat, this.dataset.lng, `${labelText}: ${this.textContent}`);
                    resultsDiv.innerHTML = '';
                });

                resultsDiv.appendChild(resultItem);
            });
        } else {
            alert(`${labelText} location not found.`);
        }
    });
}

document.getElementById("search-start").addEventListener("click", () => handleSearch("start", "result-start", "Starting point", "startCoords"));
document.getElementById("search-end").addEventListener("click", () => handleSearch("end", "result-end", "Ending point", "endCoords"));

document.getElementById("search-form").addEventListener("submit", function(event) {
    event.preventDefault();
    if (typeof startCoords == 'undefined' || typeof endCoords == 'undefined') {
        alert("Vui lòng nhập đầy đủ điểm đi và điểm đến.");
        return;
    }
    const algorithm = document.getElementById("algorithm").value;
    findRoute(startCoords, endCoords, algorithm);
});
