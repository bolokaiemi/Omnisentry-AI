
async function checkWebsite() {

    const domain =
        document.getElementById("domain").value.trim();

    if (!domain) {

        alert("Please enter a domain");
        return;
    }

    const result =
        document.getElementById("result");

    result.innerHTML =
        "<div class='card'>🔍 Scanning website...</div>";

    try {

        const response =
            await fetch(`/check/${domain}`);

        const data =
            await response.json();

        if (!data.success) {

            result.innerHTML = `
                <div class="card">
                    <h3>❌ Scan Failed</h3>
                    <p>${data.error}</p>
                </div>
            `;

            return;
        }

        const report =
            data.data;

        let scoreClass = "good";

        if (report.trust_score < 70)
            scoreClass = "medium";

        if (report.trust_score < 40)
            scoreClass = "bad";

        result.innerHTML = `
            <div class="card">

                <h2>${report.domain}</h2>

                <div class="score ${scoreClass}">
                    ${report.trust_score}/100
                </div>

                <div class="row">
                    🔒 HTTPS:
                    ${report.ssl ? "Enabled" : "Missing"}
                </div>

                <div class="row">
                    🌐 Registered:
                    ${report.registered ? "Yes" : "No"}
                </div>

                <div class="row">
                    📅 Domain Age:
                    ${report.age_days} days
                </div>

                <div class="row">
                    ⚡ Reputation:
                    ${report.reputation}
                </div>

            </div>
        `;

        if (
            "Notification" in window &&
            Notification.permission === "granted"
        ) {

            new Notification(
                "Omminsentiry AI",
                {
                    body:
                        `${report.domain} scored ${report.trust_score}/100`
                }
            );
        }

    }
    catch(error){

        result.innerHTML = `
            <div class="card">
                ❌ ${error}
            </div>
        `;
    }
}

window.onload = () => {

    if (
        "Notification" in window
    ) {

        Notification.requestPermission();
    }
};
