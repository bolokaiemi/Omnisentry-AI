// ==========================================
// MAP MODULE
// ==========================================

let omminsentiryMap = null;

function initializeMap() {

    const mapContainer =
        document.getElementById(
            "map"
        );

    if (!mapContainer) {

        return;
    }

    omminsentiryMap = L.map(
        "map"
    ).setView(
        [0, 0],
        2
    );

    L.tileLayer(
        "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            maxZoom: 19
        }
    ).addTo(
        omminsentiryMap
    );
}

function updateMap(
    latitude,
    longitude,
    label
) {

    if (!omminsentiryMap) {

        return;
    }

    omminsentiryMap.setView(
        [
            latitude,
            longitude
        ],
        10
    );

    L.marker(
        [
            latitude,
            longitude
        ]
    )
        .addTo(
            omminsentiryMap
        )
        .bindPopup(
            label
        );
}

document.addEventListener(
    "DOMContentLoaded",
    initializeMap
);