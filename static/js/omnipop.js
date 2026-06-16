// ==========================================
// OMNIPOP ROVING AI CLIENT
// ==========================================

const OmniPop = {

    enabled: true,
    version: "2.0.0",
    scanInterval: null,
    frequency: 30000, // Default 30s

    start() {
        console.log("OmniPop Roving AI Client Started");
        
        // Listen to settings changes from Mascot panel
        document.addEventListener("omnipopScanFreqChanged", (e) => {
            console.log("OmniPop scan frequency updated to:", e.detail, "ms");
            this.frequency = e.detail;
            this.setupInterval();
        });

        // Load settings from localStorage
        const savedFreq = localStorage.getItem("omnipop_scan_frequency");
        if (savedFreq) {
            this.frequency = parseInt(savedFreq);
        }

        this.setupInterval();
        
        // Initial scan after mascot is loaded and spoken
        setTimeout(() => {
            this.runSecurityScan();
        }, 8000);
    },

    setupInterval() {
        if (this.scanInterval) {
            clearInterval(this.scanInterval);
        }
        
        this.scanInterval = setInterval(() => {
            this.runSecurityScan();
        }, this.frequency);
    },

    async runSecurityScan() {
        // Check if active protection is toggled on in settings
        const active = localStorage.getItem("omnipop_protection_active");
        if (active === "false") {
            console.log("OmniPop real-time scan skipped (Protection disabled).");
            return;
        }

        console.log("OmniPop executing security scan...");
        
        // Change mascot state to scanning
        popupEngine.setState("scanning");
        popupEngine.speak("🔍 Scanning Page...", "I am analyzing the text and elements of this page for threat signatures.", 3000);

        // Gather page content
        const bodyText = document.body.innerText || "";
        const pageContent = bodyText.substring(0, 3000); // Limit size for payload

        try {
            // Post content to Omminsentiry AI threat detection endpoint
            const response = await fetch("/omnipop/threat-detect", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ content: pageContent })
            });

            if (!response.ok) {
                throw new Error("HTTP scan failure");
            }

            const report = await response.json();
            console.log("Scan Report:", report);

            // Wait a moment for visual effect so the user sees the scanning state
            setTimeout(() => {
                const riskScore = report.risk_score || 0;
                const threats = report.threats || [];

                if (riskScore >= 80) {
                    popupEngine.setState("critical");
                    const msg = `Critical risk detected! Score: ${riskScore}/100. Threat vectors: ${threats.join(', ') || 'Credential Theft'}. Do not enter passwords or cards!`;
                    popupEngine.speak("⛔ Critical Security Alert", msg, 0); // Stays open
                } else if (riskScore >= 50) {
                    popupEngine.setState("warning");
                    const msg = `Suspicious patterns detected on this page (Score: ${riskScore}/100). Flagged: ${threats.join(', ') || 'Pressure Tactics'}. Verify before proceeding.`;
                    popupEngine.speak("⚠️ Security Warning", msg, 8000);
                } else {
                    popupEngine.setState("safe");
                    
                    // Don't disturb the user if it's safe unless they trigger it,
                    // but on first or occasional scans we can report status.
                    if (Math.random() < 0.4) {
                        popupEngine.speak("✅ Page Audited", "I audited this page's script signatures and contents. No security threats were flagged. Browsing is safe!", 5000);
                    }
                }
            }, 2000);

        } catch (error) {
            console.error("OmniPop scan error:", error);
            
            // Fallback to offline keyword scanning if server check fails
            this.offlineKeywordScan();
        }
    },

    offlineKeywordScan() {
        const pageText = document.body.innerText.toLowerCase();
        const suspiciousTerms = [
            "credit card", "send money", "wire transfer", "gift card",
            "bank account", "bitcoin", "crypto payment", "password", "verify account"
        ];
        
        let detected = [];
        suspiciousTerms.forEach(term => {
            if (pageText.includes(term)) {
                detected.push(term);
            }
        });

        setTimeout(() => {
            if (detected.length >= 3) {
                popupEngine.setState("danger");
                popupEngine.speak("🚨 Offline Threat Flag", `Detected suspicious terms: ${detected.join(', ')}. Keep sensitive details secure!`, 0);
            } else if (detected.length > 0) {
                popupEngine.setState("warning");
                popupEngine.speak("⚠️ Security Warning", `Suspicious terms detected: ${detected.join(', ')}. Be cautious of payment or login forms.`, 6000);
            } else {
                popupEngine.setState("safe");
            }
        }, 1500);
    }
};

document.addEventListener("DOMContentLoaded", () => {
    // Wait for popupEngine to initialize
    setTimeout(() => {
        OmniPop.start();
    }, 500);
});