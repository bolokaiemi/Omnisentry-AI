// ==========================================
// OMMINSENTIRY AI
// MAIN APPLICATION
// ==========================================

async function checkWebsite() {
    const domainInput = document.getElementById("domain");
    const domain = domainInput.value.trim().replace(/^(https?:\/\/)?(www\.)?/, ""); // Clean domain input

    if (!domain) {
        alert("Please enter a domain.");
        return;
    }

    const result = document.getElementById("result");
    result.innerHTML = `
        <div class="card" style="text-align: center; padding: 40px 20px;">
            <div class="spinner" style="border: 4px solid rgba(255,255,255,0.1); border-top: 4px solid #3b82f6; border-radius: 50%; width: 40px; height: 40px; margin: 0 auto 15px auto; animation: spin 1s linear infinite;"></div>
            <p style="font-size: 1.1rem; color: #94a3b8;">🔍 Analyzing domain registration, SSL certificates, threat databases, and geolocation...</p>
        </div>
        <style>
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        </style>
    `;

    try {
        const response = await fetch(`/check/${domain}`);
        const data = await response.json();

        if (!data.success) {
            result.innerHTML = `
                <div class="card" style="border-color: #ef4444; background: rgba(239,68,68,0.05);">
                    <h3 style="color: #ef4444; margin-bottom: 8px;">❌ Scan Failed</h3>
                    <p style="color: #fca5a5;">${data.error}</p>
                </div>
            `;
            return;
        }

        const report = data.data;

        // Log threat telemetry to the dashboard database
        if (typeof popupEngine !== "undefined" && popupEngine !== null) {
            popupEngine.trackThreat(report.domain, report.risk_level, report.risk_factors.join(', ') || 'Domain Security Audit');
        }

        // Visual score class
        let scoreClass = "score-good";
        let badgeClass = "badge-safe";
        if (report.trust_score < 85) {
            badgeClass = "badge-low";
        }
        if (report.trust_score < 70) {
            scoreClass = "score-medium";
            badgeClass = "badge-medium";
        }
        if (report.trust_score < 40) {
            scoreClass = "score-bad";
            badgeClass = "badge-high";
        }
        if (report.trust_score < 15) {
            scoreClass = "score-bad";
            badgeClass = "badge-critical";
        }

        // Compile risk factors HTML
        let factorsHtml = "";
        if (report.risk_factors && report.risk_factors.length > 0) {
            factorsHtml = `
                <div style="margin-top: 20px;">
                    <h4 style="color: #fca5a5; font-size: 1rem; margin-bottom: 8px;">Detected Risk Factors:</h4>
                    <div class="factors-list">
                        ${report.risk_factors.map(factor => `
                            <div class="factor-item">
                                ⚠️ ${factor}
                            </div>
                        `).join("")}
                    </div>
                </div>
            `;
        } else {
            factorsHtml = `
                <div style="margin-top: 20px;">
                    <div class="factor-item-safe">
                        ✅ No critical security threats or risk factors were detected.
                    </div>
                </div>
            `;
        }

        // AI assessment status
        let aiHtml = "";
        if (report.ai_prediction !== null) {
            const aiVerdict = report.ai_prediction === 1 
                ? "<span style='color: #10b981; font-weight: bold;'>TRUSTED</span>" 
                : "<span style='color: #ef4444; font-weight: bold;'>UNTRUSTED / RISKY</span>";
            aiHtml = `<div class="data-row"><strong>AI Model Verdict:</strong> <span>${aiVerdict}</span></div>`;
        }

        result.innerHTML = `
            <div class="card">
                <div class="score-display">
                    <div class="score-circle ${scoreClass}">
                        ${report.trust_score}
                        <span>/ 100</span>
                    </div>
                    <div class="score-text-details">
                        <h2>🌐 ${report.domain}</h2>
                        <div>
                            <span class="badge ${badgeClass}">${report.risk_level}</span>
                            <span class="badge ${report.ssl ? 'badge-safe' : 'badge-high'}">${report.ssl ? 'SSL SECURE' : 'NO SSL'}</span>
                        </div>
                    </div>
                </div>

                <div class="grid-cols">
                    <div>
                        <h3 style="margin-bottom: 12px; font-size: 1.1rem; color: #3b82f6;">Domain Information</h3>
                        <div class="data-row"><strong>Registration:</strong> <span>${report.registered ? '✅ Registered' : '❌ Unregistered'}</span></div>
                        <div class="data-row"><strong>Domain Age:</strong> <span>${report.age_days} days</span></div>
                        <div class="data-row"><strong>Registrar:</strong> <span>${report.registrar || 'Unknown'}</span></div>
                        <div class="data-row"><strong>Created On:</strong> <span>${report.creation_date || 'Unknown'}</span></div>
                    </div>
                    <div>
                        <h3 style="margin-bottom: 12px; font-size: 1.1rem; color: #3b82f6;">Server Location</h3>
                        <div class="data-row"><strong>IP Address:</strong> <span>${report.ip_address || 'Unknown'}</span></div>
                        <div class="data-row"><strong>Location:</strong> <span>${report.city || 'Unknown'}, ${report.country || 'Unknown'}</span></div>
                        <div class="data-row"><strong>ISP:</strong> <span>${report.isp || 'Unknown'}</span></div>
                        ${aiHtml}
                    </div>
                </div>

                ${factorsHtml}

                <div class="action-buttons">
                    <a href="/report/view/${report.domain}" class="btn btn-primary" target="_blank">📊 View Detailed HTML Report</a>
                    <a href="/map?lat=${report.latitude || 0}&lon=${report.longitude || 0}&domain=${report.domain}&country=${report.country || 'Unknown'}&city=${report.city || 'Unknown'}&risk=${encodeURIComponent(report.risk_level)}&score=${report.trust_score}&ip=${report.ip_address || ''}&isp=${encodeURIComponent(report.isp || '')}" class="btn btn-secondary">🌍 Interactive Map</a>
                    <button onclick="downloadReportJson('${report.domain}')" class="btn btn-success">📥 Export Report (JSON)</button>
                </div>

                <div class="share-result-deck" style="margin-top: 20px; padding-top: 15px; border-top: 1px solid var(--border-color); display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                    <span style="font-size: 0.85rem; color: var(--text-secondary); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Share Result:</span>
                    <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                        <a href="https://api.whatsapp.com/send?text=${encodeURIComponent('Website Security Audit for ' + report.domain + ' on Omminsentiry AI:\n' + (report.risk_level === 'SAFE' ? '🟢 SAFE' : '⚠️ WARNING: ' + report.risk_level) + ' (Score: ' + report.trust_score + '/100).\nDetails: ' + window.location.origin + '/report/view/' + report.domain)}" class="share-btn-sm whatsapp" style="text-decoration: none; padding: 6px 12px; border-radius: 8px; font-size: 0.8rem; font-weight: 600; display: inline-flex; align-items: center; gap: 4px;" target="_blank">💬 WhatsApp</a>
                        <a href="https://twitter.com/intent/tweet?text=${encodeURIComponent('Website Security Audit for ' + report.domain + ' on Omminsentiry AI:\n' + (report.risk_level === 'SAFE' ? '🟢 SAFE' : '⚠️ WARNING: ' + report.risk_level) + ' (Score: ' + report.trust_score + '/100).\nDetails: ' + window.location.origin + '/report/view/' + report.domain)}" class="share-btn-sm twitter" style="text-decoration: none; padding: 6px 12px; border-radius: 8px; font-size: 0.8rem; font-weight: 600; display: inline-flex; align-items: center; gap: 4px;" target="_blank">🐦 X (Twitter)</a>
                        <a href="https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(window.location.origin + '/report/view/' + report.domain)}" class="share-btn-sm facebook" style="text-decoration: none; padding: 6px 12px; border-radius: 8px; font-size: 0.8rem; font-weight: 600; display: inline-flex; align-items: center; gap: 4px;" target="_blank">📘 Facebook</a>
                        <a href="https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(window.location.origin + '/report/view/' + report.domain)}" class="share-btn-sm linkedin" style="text-decoration: none; padding: 6px 12px; border-radius: 8px; font-size: 0.8rem; font-weight: 600; display: inline-flex; align-items: center; gap: 4px;" target="_blank">💼 LinkedIn</a>
                    </div>
                </div>
            </div>
        `;

        // Push desktop notification if permitted
        if ("Notification" in window && Notification.permission === "granted") {
            new Notification("Omminsentiry AI Scan Complete", {
                body: `${report.domain} is classified as ${report.risk_level} (Score: ${report.trust_score}/100)`
            });
        }

    } catch (error) {
        result.innerHTML = `
            <div class="card" style="border-color: #ef4444; background: rgba(239,68,68,0.05);">
                <h3 style="color: #ef4444; margin-bottom: 8px;">❌ Connection Error</h3>
                <p style="color: #fca5a5;">${error.message}</p>
            </div>
        `;
    }
}

// Download JSON utility
async function downloadReportJson(domain) {
    try {
        const response = await fetch(`/report/${domain}`);
        const data = await response.json();
        if (data.success) {
            const jsonStr = JSON.stringify(data.report, null, 2);
            const blob = new Blob([jsonStr], { type: "application/json" });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `Omminsentiry_AI_Report_${domain}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        } else {
            alert("Failed to export report: " + data.error);
        }
    } catch(err) {
        alert("Export failed: " + err.message);
    }
}

// ==========================================
// PAGE LOAD
// ==========================================

window.onload = () => {
    if ("Notification" in window) {
        Notification.requestPermission();
    }

    const domainInput = document.getElementById("domain");
    if (domainInput) {
        domainInput.addEventListener("keypress", function(event) {
            if (event.key === "Enter") {
                checkWebsite();
            }
        });
    }
};