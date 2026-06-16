let scannedDomains = 0;
let reportsSent = 0;

document.addEventListener("DOMContentLoaded", () => {
    initializeRover();
});

function initializeRover() {
    console.log("OmniRover Initialized");

    updateDashboard();

    setInterval(() => {
        autoScan();
    }, 5000);
}

function startRover() {
    const status = document.getElementById("rover-status");

    if (status) {
        status.textContent = "SCANNING";
    }

    notify("🚀 OmniRover started scanning");
}

function autoScan() {
    scannedDomains += Math.floor(Math.random() * 3);

    updateDashboard();
}

function simulateThreat() {
    const threatLevel =
        document.getElementById("threat-level");

    const threatFeed =
        document.getElementById("threat-feed");

    reportsSent += 1;

    if (threatLevel) {
        threatLevel.textContent = "HIGH";
    }

    if (threatFeed) {
        const alertBox = document.createElement("p");

        alertBox.textContent =
            "⚠ Phishing threat detected and reported.";

        threatFeed.prepend(alertBox);
    }

    updateDashboard();

    showPopupWarning();
}

function updateDashboard() {
    const scanned =
        document.getElementById("domains-scanned");

    const reports =
        document.getElementById("reports-sent");

    if (scanned) {
        scanned.textContent = scannedDomains;
    }

    if (reports) {
        reports.textContent = reportsSent;
    }
}

function showPopupWarning() {
    const warning = document.createElement("div");

    warning.style.position = "fixed";
    warning.style.top = "20px";
    warning.style.right = "20px";
    warning.style.padding = "20px";
    warning.style.background = "#ff4d4f";
    warning.style.color = "white";
    warning.style.borderRadius = "10px";
    warning.style.zIndex = "9999";
    warning.style.boxShadow =
        "0 0 15px rgba(0,0,0,0.3)";

    warning.textContent =
        "⚠ OmniRover Warning: Do NOT enter payment details on this website.";

    document.body.appendChild(warning);

    setTimeout(() => {
        warning.remove();
    }, 5000);
}

function notify(message) {
    console.log(message);
}