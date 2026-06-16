document.addEventListener("DOMContentLoaded", () => {
    initializeMobileDashboard();
});

function initializeMobileDashboard() {
    console.log("OmniRover Mobile Sync Started");

    syncDevice();

    setInterval(() => {
        syncDevice();
    }, 10000);
}

function syncDevice() {
    const threatCount = document.getElementById("threat-count");
    const alertsList = document.getElementById("alerts-list");

    const randomThreats = Math.floor(Math.random() * 4);

    if (threatCount) {
        threatCount.textContent = randomThreats;
    }

    if (alertsList) {
        alertsList.innerHTML = "";

        if (randomThreats === 0) {
            alertsList.innerHTML =
                "<li>✅ No threats detected</li>";
        } else {
            for (let i = 0; i < randomThreats; i++) {
                const li = document.createElement("li");
                li.textContent =
                    "⚠ Suspicious website activity detected";
                alertsList.appendChild(li);
            }
        }
    }

    console.log("Device synced");
}