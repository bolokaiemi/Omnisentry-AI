
// ==========================================
// OMMINSENTIRY AI
// MAIN APPLICATION
// ==========================================

async function checkWebsite() {

    const domain =
        document
        .getElementById("domain")
        .value
        .trim();

    if (!domain) {

        alert(
            "Please enter a domain."
        );

        return;
    }

    const result =
        document.getElementById(
            "result"
        );

    result.innerHTML = `
        <div class="card">
            🔍 Scanning website...
        </div>
    `;

    try {

        const response =
            await fetch(
                `/check/${domain}`
            );

        const data =
            await response.json();

        if (!data.success) {

            result.innerHTML = `
                <div class="card">
                    ❌ ${data.error}
                </div>
            `;

            return;
        }

        const report =
            data.data;

        let scoreClass =
            "good";

        if (
            report.trust_score < 70
        ){
            scoreClass =
                "medium";
        }

        if (
            report.trust_score < 40
        ){
            scoreClass =
                "bad";
        }

        result.innerHTML = `

            <div class="card">

                <h2>
                    🌐 ${report.domain}
                </h2>

                <div class="score ${scoreClass}">
                    ${report.trust_score}/100
                </div>

                <div class="row">
                    SSL:
                    ${report.ssl
                        ? "✅ Enabled"
                        : "❌ Missing"}
                </div>

                <div class="row">
                    Registered:
                    ${report.registered
                        ? "✅ Yes"
                        : "❌ No"}
                </div>

                <div class="row">
                    Domain Age:
                    ${report.age_days} days
                </div>

                <div class="row">
                    Reputation:
                    ${report.reputation}
                </div>

                <div class="row">
                    Risk Level:
                    ${report.risk_level || "Unknown"}
                </div>

                <div class="row">
                    IP Address:
                    ${report.ip_address || "Unknown"}
                </div>

                <div class="row">
                    Country:
                    ${report.country || "Unknown"}
                </div>

                <div class="row">
                    City:
                    ${report.city || "Unknown"}
                </div>

            </div>

        `;

        if (
            "Notification" in window &&
            Notification.permission === "granted"
        ){

            new Notification(
                "Omminsentiry AI Scan Complete",
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
                ❌ Error:
                ${error.message}
            </div>
        `;
    }
}

// ==========================================
// PAGE LOAD
// ==========================================

window.onload = () => {

    if (
        "Notification" in window
    ){

        Notification.requestPermission();
    }

    const domainInput =
        document.getElementById(
            "domain"
        );

    if(domainInput){

        domainInput.addEventListener(
            "keypress",
            function(event){

                if(
                    event.key === "Enter"
                ){

                    checkWebsite();
                }
            }
        );
    }
};
