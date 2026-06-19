// ==========================================
// OMMNISENTRY AI
// OMNIPOP POPUP ENGINE (ROVING AI MASCOT)
// ==========================================

class PopupEngine {

    constructor() {
        this.container = null;
        this.speechBubble = null;
        this.settingsPanel = null;
        this.avatar = null;
        
        this.isDragging = false;
        this.dragStartX = 0;
        this.dragStartY = 0;
        this.mascotLeft = 0;
        this.mascotTop = 0;
        
        // Roving settings
        this.rovingEnabled = true;
        this.rovingInterval = null;
        this.speechTimeout = null;
        this.currentState = "idle"; // idle, safe, warning, danger, critical, scanning

        this.init();
    }

    // ======================================
    // INITIALIZATION & DOM INJECTION
    // ======================================

    init() {
        // Ensure DOM is loaded
        if (document.readyState === "loading") {
            document.addEventListener("DOMContentLoaded", () => this.injectMascot());
        } else {
            this.injectMascot();
        }
    }

    injectMascot() {
        if (document.getElementById("omnipop-mascot-container")) return;

        // Create container
        this.container = document.createElement("div");
        this.container.id = "omnipop-mascot-container";
        this.container.className = "state-safe"; // Default safe state

        // Restore position or set default (bottom right)
        const savedLeft = localStorage.getItem("omnipop_mascot_left");
        const savedTop = localStorage.getItem("omnipop_mascot_top");
        if (savedLeft && savedTop) {
            this.container.style.left = savedLeft;
            this.container.style.top = savedTop;
            this.container.style.bottom = "auto";
            this.container.style.right = "auto";
        } else {
            this.container.style.bottom = "30px";
            this.container.style.right = "30px";
        }

        // Inner HTML structure
        this.container.innerHTML = `
            <!-- Speech Bubble -->
            <div id="omnipop-speech-bubble" class="omnipop-speech-bubble">
                <div class="bubble-header" id="bubble-header">
                    <span>🛡️ OmniRover AI</span>
                </div>
                <div id="bubble-text">System initialized. Monitoring page security...</div>
            </div>

            <!-- Settings Panel -->
            <div id="omnipop-mascot-panel" class="mascot-panel">
                <h3>⚙️ Roving AI Settings <span class="mascot-panel-close" id="mascot-panel-close">✖</span></h3>
                <div class="panel-row">
                    <span>Active Protection</span>
                    <label class="switch">
                        <input type="checkbox" id="toggle-protection" checked>
                        <span class="slider"></span>
                    </label>
                </div>
                <div class="panel-row">
                    <span>Auto Roving (Wander)</span>
                    <label class="switch">
                        <input type="checkbox" id="toggle-roving" checked>
                        <span class="slider"></span>
                    </label>
                </div>
                <div class="panel-row">
                    <span>Scan Frequency</span>
                    <select id="select-scan" style="background:#1e293b; color:white; border:1px solid rgba(255,255,255,0.2); border-radius:4px; padding:2px 6px; font-size:0.8rem;">
                        <option value="10000">10 seconds</option>
                        <option value="30000" selected>30 seconds</option>
                        <option value="60000">1 minute</option>
                    </select>
                </div>
                <button id="mascot-reset-pos" class="btn btn-primary" style="width:100%; padding:6px; font-size:0.8rem; margin-top:10px;">Reset Mascot Position</button>
            </div>

            <!-- Minimize Button -->
            <div class="mascot-close-btn" id="mascot-close-btn" title="Hide AI Assistant">✖</div>
            
            <!-- Settings Button -->
            <div class="mascot-settings-btn" id="mascot-settings-btn" title="Configure AI">⚙️</div>

            <!-- Mascot Avatar -->
            <div class="mascot-wrapper" id="mascot-wrapper">
                <div class="omnipop-pulse-ring"></div>
                <img src="/static/image/omnipop_mascot.png" class="mascot-avatar" alt="OmniPop Security Mascot" id="mascot-avatar-img">
            </div>
        `;

        document.body.appendChild(this.container);

        // Bind DOM elements
        this.speechBubble = document.getElementById("omnipop-speech-bubble");
        this.settingsPanel = document.getElementById("omnipop-mascot-panel");
        this.avatar = document.getElementById("mascot-avatar-img");

        // Event Listeners
        this.setupDragging();
        this.setupControlPanel();
        
        // Load settings from localStorage
        this.loadSettings();

        // Start behaviors
        this.startRoving();
        
        // Welcome message
        setTimeout(() => {
            this.speak("🛡️ OmniRover AI", "Hello! I am OmniRover. I will wander around this page to monitor security threats in real-time.", 6000);
        }, 1500);
    }

    // ======================================
    // DRAGGABLE MECHANICS
    // ======================================

    setupDragging() {
        const wrapper = document.getElementById("mascot-wrapper");

        const onStart = (e) => {
            if (e.target.closest(".mascot-settings-btn") || e.target.closest(".mascot-close-btn") || e.target.closest(".mascot-panel") || e.target.closest(".omnipop-speech-bubble")) {
                return;
            }
            
            this.isDragging = true;
            this.container.classList.remove("roving");
            
            const clientX = e.type === "touchstart" ? e.touches[0].clientX : e.clientX;
            const clientY = e.type === "touchstart" ? e.touches[0].clientY : e.clientY;
            
            const rect = this.container.getBoundingClientRect();
            
            this.dragStartX = clientX - rect.left;
            this.dragStartY = clientY - rect.top;
            
            e.preventDefault();
        };

        const onMove = (e) => {
            if (!this.isDragging) return;

            const clientX = e.type === "touchmove" ? e.touches[0].clientX : e.clientX;
            const clientY = e.type === "touchmove" ? e.touches[0].clientY : e.clientY;

            let left = clientX - this.dragStartX;
            let top = clientY - this.dragStartY;

            // Contain within viewport boundaries
            const minX = 10;
            const maxX = window.innerWidth - 90;
            const minY = 10;
            const maxY = window.innerHeight - 90;

            left = Math.max(minX, Math.min(left, maxX));
            top = Math.max(minY, Math.min(top, maxY));

            this.container.style.bottom = "auto";
            this.container.style.right = "auto";
            this.container.style.left = `${left}px`;
            this.container.style.top = `${top}px`;

            this.mascotLeft = left;
            this.mascotTop = top;
        };

        const onEnd = () => {
            if (this.isDragging) {
                this.isDragging = false;
                // Save drag coordinates
                localStorage.setItem("omnipop_mascot_left", this.container.style.left);
                localStorage.setItem("omnipop_mascot_top", this.container.style.top);
                
                // Briefly pause roving to let user interact
                this.pauseRovingTemporarily();
            }
        };

        wrapper.addEventListener("mousedown", onStart);
        wrapper.addEventListener("touchstart", onStart, { passive: false });

        document.addEventListener("mousemove", onMove);
        document.addEventListener("touchmove", onMove, { passive: false });

        document.addEventListener("mouseup", onEnd);
        document.addEventListener("touchend", onEnd);
    }

    // ======================================
    // CONTROL PANEL & SETTINGS
    // ======================================

    setupControlPanel() {
        const settingsBtn = document.getElementById("mascot-settings-btn");
        const closeBtn = document.getElementById("mascot-close-btn");
        const panelClose = document.getElementById("mascot-panel-close");
        const resetPosBtn = document.getElementById("mascot-reset-pos");
        
        const toggleRoving = document.getElementById("toggle-roving");
        const toggleProtection = document.getElementById("toggle-protection");
        const selectScan = document.getElementById("select-scan");

        // Toggle panel visibility
        settingsBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            this.settingsPanel.classList.toggle("active");
            this.speechBubble.classList.remove("active");
        });

        panelClose.addEventListener("click", () => {
            this.settingsPanel.classList.remove("active");
        });

        // Hide mascot entirely
        closeBtn.addEventListener("click", () => {
            this.speak("👋 Goodbye", "I will hide now. Refresh the page to bring me back!", 3000);
            setTimeout(() => {
                this.container.style.display = "none";
            }, 3000);
        });

        // Reset position to bottom right
        resetPosBtn.addEventListener("click", () => {
            localStorage.removeItem("omnipop_mascot_left");
            localStorage.removeItem("omnipop_mascot_top");
            
            this.container.classList.add("roving");
            this.container.style.left = "";
            this.container.style.top = "";
            this.container.style.bottom = "30px";
            this.container.style.right = "30px";
            
            this.settingsPanel.classList.remove("active");
            this.speak("📍 Repositioned", "I am back in my cozy bottom-right corner!", 3000);
        });

        // Save settings on changes
        toggleRoving.addEventListener("change", (e) => {
            this.rovingEnabled = e.target.checked;
            localStorage.setItem("omnipop_roving_enabled", this.rovingEnabled);
            if (this.rovingEnabled) {
                this.startRoving();
            } else {
                this.stopRoving();
            }
        });

        toggleProtection.addEventListener("change", (e) => {
            const active = e.target.checked;
            localStorage.setItem("omnipop_protection_active", active);
            if (active) {
                this.speak("🛡️ Protection Enabled", "Real-time threat monitoring is fully active.", 3000);
            } else {
                this.speak("⚠️ Protection Disabled", "I will stop scanning this page.", 3000);
                this.setState("safe");
            }
        });

        selectScan.addEventListener("change", (e) => {
            const freq = e.target.value;
            localStorage.setItem("omnipop_scan_frequency", freq);
            // Dispatch event for omnipop.js to reload scan interval
            const event = new CustomEvent("omnipopScanFreqChanged", { detail: parseInt(freq) });
            document.dispatchEvent(event);
        });

        // Clicking avatar toggles speech bubble
        document.getElementById("mascot-wrapper").addEventListener("click", () => {
            if (!this.isDragging) {
                this.speechBubble.classList.toggle("active");
            }
        });
    }

    loadSettings() {
        const savedRoving = localStorage.getItem("omnipop_roving_enabled");
        if (savedRoving !== null) {
            this.rovingEnabled = savedRoving === "true";
            document.getElementById("toggle-roving").checked = this.rovingEnabled;
        }

        const savedProtection = localStorage.getItem("omnipop_protection_active");
        if (savedProtection !== null) {
            const active = savedProtection === "true";
            document.getElementById("toggle-protection").checked = active;
        }

        const savedFreq = localStorage.getItem("omnipop_scan_frequency");
        if (savedFreq !== null) {
            document.getElementById("select-scan").value = savedFreq;
        }
    }

    // ======================================
    // DIALOGUE & SPEECH MECHANICS
    // ======================================

    speak(title, message, duration = 5000) {
        if (!this.speechBubble) return;

        // Clear any previous speech timeouts
        if (this.speechTimeout) {
            clearTimeout(this.speechTimeout);
        }

        const headerSpan = document.getElementById("bubble-header");
        const textDiv = document.getElementById("bubble-text");

        headerSpan.innerHTML = title;
        textDiv.innerHTML = message;

        // Trigger float-up fade-in animation
        this.speechBubble.classList.add("active");

        if (duration > 0) {
            this.speechTimeout = setTimeout(() => {
                this.speechBubble.classList.remove("active");
            }, duration);
        }
    }

    // ======================================
    // STATE MACHINE
    // ======================================

    setState(state) {
        if (!this.container) return;

        // Remove all previous states
        this.container.classList.remove("state-safe", "state-warning", "state-danger", "state-critical", "state-scanning");
        
        // Apply new state
        this.currentState = state;
        this.container.classList.add(`state-${state}`);
    }

    // ======================================
    // AUTO-ROVING / WANDERING MECHANICS
    // ======================================

    startRoving() {
        this.stopRoving();
        if (!this.rovingEnabled) return;

        // Rove every 12 seconds
        this.rovingInterval = setInterval(() => {
            this.glideToRandomPosition();
        }, 12000);
    }

    stopRoving() {
        if (this.rovingInterval) {
            clearInterval(this.rovingInterval);
            this.rovingInterval = null;
        }
    }

    pauseRovingTemporarily() {
        this.stopRoving();
        setTimeout(() => {
            if (this.rovingEnabled) {
                this.startRoving();
            }
        }, 20000); // Wait 20 seconds before resuming auto-wander
    }

    glideToRandomPosition() {
        if (this.isDragging || !this.container) return;

        // Enable gliding transition
        this.container.classList.add("roving");

        // Calculate random screen position bounded
        const mascotWidth = 90;
        const mascotHeight = 90;
        
        const padding = 60;
        const minX = padding;
        const maxX = window.innerWidth - mascotWidth - padding;
        const minY = padding;
        const maxY = window.innerHeight - mascotHeight - padding;

        const targetX = Math.floor(Math.random() * (maxX - minX + 1)) + minX;
        const targetY = Math.floor(Math.random() * (maxY - minY + 1)) + minY;

        // Apply new styles
        this.container.style.bottom = "auto";
        this.container.style.right = "auto";
        this.container.style.left = `${targetX}px`;
        this.container.style.top = `${targetY}px`;

        this.mascotLeft = targetX;
        this.mascotTop = targetY;

        // Say something friendly occasionally during travel
        const sayings = [
            "Just cruising around to check site assets... 🛰️",
            "Scanning elements from a different angle! 🔍",
            "Everything looks clear here. Moving along! 🛡️",
            "Checking scripts and connections... ⚙️",
            "OmniRover on patrol! 🤖"
        ];
        
        // 30% chance to speak when roving
        if (Math.random() < 0.3 && this.currentState === "safe") {
            const randomSaying = sayings[Math.floor(Math.random() * sayings.length)];
            setTimeout(() => {
                this.speak("🤖 OmniRover", randomSaying, 4000);
            }, 1000);
        }
    }

    // ======================================
    // THREAT TELEMETRY & DATABASE LOGGING
    // ======================================

    trackThreat(domain, riskLevel, threatType) {
        // Increment global counters
        let threats = parseInt(localStorage.getItem("omnipop_threats") || "0");
        let warnings = parseInt(localStorage.getItem("omnipop_warnings") || "0");
        let highrisk = parseInt(localStorage.getItem("omnipop_highrisk") || "0");

        threats++;
        const rl = riskLevel.toLowerCase();
        if (rl === "warning" || rl === "medium risk" || rl === "medium") {
            warnings++;
        } else if (rl === "danger" || rl === "critical" || rl === "high risk" || rl === "critical risk" || rl === "high") {
            highrisk++;
        }

        localStorage.setItem("omnipop_threats", threats);
        localStorage.setItem("omnipop_warnings", warnings);
        localStorage.setItem("omnipop_highrisk", highrisk);

        // Add to recent reports list
        let reports = [];
        try {
            reports = JSON.parse(localStorage.getItem("omnipop_reports") || "[]");
        } catch (e) {
            reports = [];
        }

        const newReport = {
            domain: domain,
            risk: riskLevel.toUpperCase(),
            type: threatType,
            time: new Date().toLocaleString()
        };

        // Prepend new report and limit to last 10
        reports.unshift(newReport);
        if (reports.length > 10) {
            reports = reports.slice(0, 10);
        }

        localStorage.setItem("omnipop_reports", JSON.stringify(reports));

        // Dispatch custom event to notify open dashboard components
        document.dispatchEvent(new CustomEvent("omnipopThreatsUpdated"));
    }

    // ======================================
    // PUBLIC API (BACKWARDS COMPATIBILITY)
    // ======================================

    showSafe() {
        this.setState("safe");
        this.speak("✅ Website Safe", "No significant threat patterns or scam vectors were found on this domain.", 6000);
    }

    showWarning(message) {
        this.setState("warning");
        this.speak("⚠️ Security Warning", message, 8000);
        this.trackThreat(window.location.hostname || "local-simulation", "warning", "Urgent Language / Pattern");
    }

    showDanger(message) {
        this.setState("danger");
        this.speak("🚨 High Risk Warning", message, 0); // Stays open
        this.trackThreat(window.location.hostname || "local-simulation", "danger", "Phishing / Scam Alert");
    }

    showCritical(message) {
        this.setState("critical");
        this.speak("⛔ Critical Security Alert", message, 0); // Stays open
        this.trackThreat(window.location.hostname || "local-simulation", "critical", "Malicious Domain / Hijack");
    }
}

// ==========================================
// GLOBAL INSTANCE
// ==========================================

const popupEngine = new PopupEngine();

// ==========================================
// HELPER COMPATIBILITY WRAPPERS
// ==========================================

function showOmniPopWarning(message = "This page may be attempting to collect sensitive information.") {
    popupEngine.showWarning(message);
}

function showOmniPopDanger(message = "Do not enter passwords, banking details, or credit card information.") {
    popupEngine.showDanger(message);
}

function showOmniPopCritical(message = "This website appears highly suspicious. Leave immediately.") {
    popupEngine.showCritical(message);
}