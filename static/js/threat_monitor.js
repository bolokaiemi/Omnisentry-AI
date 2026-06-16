// ==========================================
// THREAT MONITOR
// ==========================================

class ThreatMonitor {

    constructor() {

        this.threats = [];
    }

    addThreat(

        threat

    ) {

        this.threats.push(
            {
                threat:
                    threat,

                timestamp:
                    new Date()
                        .toISOString()
            }
        );

        console.log(
            "Threat Detected:",
            threat
        );
    }

    getThreats() {

        return this.threats;
    }

}

const threatMonitor =
    new ThreatMonitor();