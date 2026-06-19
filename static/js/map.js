// ==========================================
// MAP MODULE
// ==========================================

let omnisentryMap = null;

function initializeMap() {

    const mapContainer =
        document.getElementById(
            "map"
        );

    if (!mapContainer) {

        return;
    }

   omnisentryMap = L.map(
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
        omnisentryMap
    );
}

function updateMap(
    latitude,
    longitude,
    label
) {

    if (! omnisentryMap) {

        return;
    }

     omnisentryMap.setView(
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
            omnisentryMap
        )
        .bindPopup(
            label
        );
}

document.addEventListener(
    "DOMContentLoaded",
    initializeMap
);