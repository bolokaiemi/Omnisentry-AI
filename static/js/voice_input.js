// ==========================================
// OMNINSENTRY AI
// SPEECH RECOGNITION (VOICE INPUT) SYSTEM
// ==========================================

class VoiceInputSystem {
    constructor() {
        this.recognition = null;
        this.isListening = false;
        this.activeTarget = null;
        this.activeBtn = null;
    }

    init() {
        // Check browser support
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            console.warn("Omnisentry AI Voice Input: Web Speech API is not supported in this browser.");
            // Gracefully hide mic buttons
            document.querySelectorAll(".mic-btn, .mic-btn-sm").forEach(btn => {
                btn.style.display = "none";
            });
            return;
        }

        this.recognition = new SpeechRecognition();
        this.recognition.continuous = false;
        this.recognition.interimResults = false;
        
        // Match browser recognition language with selected platform language
        this.recognition.lang = this.getLangCode(localStorage.getItem("omni_lang") || "en");

        // Event hooks
        this.recognition.onstart = () => this.handleStart();
        this.recognition.onresult = (e) => this.handleResult(e);
        this.recognition.onerror = (e) => this.handleError(e);
        this.recognition.onend = () => this.handleEnd();

        // Listen for language changes to adjust recognition language dynamically
        window.addEventListener("languagechanged", (e) => {
            if (this.recognition) {
                this.recognition.lang = this.getLangCode(e.detail.lang);
            }
        });

        // Setup DOM click bindings
        this.setupBindings();
    }

    getLangCode(omniLang) {
        const langMap = {
            en: "en-US",
            es: "es-ES",
            fr: "fr-FR",
            de: "de-DE",
            pt: "pt-PT",
            zh: "zh-CN",
            ja: "ja-JP",
            yo: "yo-NG"
        };
        return langMap[omniLang] || "en-US";
    }

    setupBindings() {
        // 1. Search Box Voice binding
        const searchMicBtn = document.getElementById("voice-search-btn");
        const domainInput = document.getElementById("domain");
        if (searchMicBtn && domainInput) {
            searchMicBtn.addEventListener("click", () => {
                this.toggleListening(domainInput, searchMicBtn, "domain");
            });
        }

        // 2. Feedback Comment Voice binding
        const commentMicBtn = document.getElementById("voice-comment-btn");
        const commentTextarea = document.getElementById("review-comment");
        if (commentMicBtn && commentTextarea) {
            commentMicBtn.addEventListener("click", () => {
                this.toggleListening(commentTextarea, commentMicBtn, "comment");
            });
        }
    }

    toggleListening(targetInput, micBtn, mode) {
        if (this.isListening) {
            this.recognition.stop();
            if (this.activeBtn === micBtn) {
                return;
            }
        }

        this.activeTarget = targetInput;
        this.activeBtn = micBtn;
        this.mode = mode; // 'domain' or 'comment'
        
        try {
            this.recognition.start();
        } catch (err) {
            console.error("Speech recognition start failed:", err);
        }
    }

    handleStart() {
        this.isListening = true;
        if (this.activeBtn) {
            this.activeBtn.classList.add("listening");
            
            // Get translation helper
            const translationEngine = window.omniI18n;
            const hintKey = this.mode === "domain" ? "voice_search_ready" : "voice_comment_ready";
            const defaultText = this.mode === "domain" ? "Speak domain..." : "Listening...";
            
            const hintText = translationEngine ? translationEngine.translate(hintKey, defaultText) : defaultText;
            this.activeBtn.title = hintText;
            
            // Temporary visual placeholder/status indicator on target field
            if (this.mode === "domain") {
                this.originalPlaceholder = this.activeTarget.placeholder;
                this.activeTarget.placeholder = "🎤 " + hintText;
            }
        }
    }

    handleResult(event) {
        const transcript = event.results[0][0].transcript;
        if (this.activeTarget) {
            if (this.mode === "domain") {
                // Clean the spoken text to make a valid domain
                const cleanedDomain = this.sanitizeDomainSpeech(transcript);
                this.activeTarget.value = cleanedDomain;
                
                // Highlight input
                this.activeTarget.focus();
            } else {
                // Append or insert comment at cursor position
                const startPos = this.activeTarget.selectionStart;
                const endPos = this.activeTarget.selectionEnd;
                const origVal = this.activeTarget.value;
                
                const before = origVal.substring(0, startPos);
                const after = origVal.substring(endPos, origVal.length);
                const addText = (startPos === 0 ? "" : " ") + transcript;
                
                this.activeTarget.value = before + addText + after;
                this.activeTarget.focus();
                
                // Move cursor to end of inserted text
                const newCursorPos = startPos + addText.length;
                this.activeTarget.setSelectionRange(newCursorPos, newCursorPos);
            }
        }
    }

    sanitizeDomainSpeech(speech) {
        let text = speech.trim().toLowerCase();
        
        // Remove protocol prefixes if spoken
        text = text.replace(/^(https?|http|ftp)\s*colon\s*slash\s*slash\s*/i, "");
        text = text.replace(/^(https?|http|ftp):\/\//i, "");
        
        // Replace spaces around "dot" to represent actual domain formatting
        text = text.replace(/\s+dot\s+/g, ".");
        text = text.replace(/\s+dot$/g, ".");
        text = text.replace(/dot\s+/g, ".");
        text = text.replace(/\s+dot/g, ".");
        text = text.replace(/(\w+)\s+dot\s+(\w+)/g, "$1.$2");
        
        // Replace Yoruba dot translation if spoken ("koko")
        text = text.replace(/\s+koko\s+/g, ".");
        
        // Remove all spaces remaining
        text = text.replace(/\s+/g, "");
        
        return text;
    }

    handleError(event) {
        console.error("Speech recognition error:", event.error);
    }

    handleEnd() {
        this.isListening = false;
        if (this.activeBtn) {
            this.activeBtn.classList.remove("listening");
            
            // Restore titles & placeholders
            this.activeBtn.title = "Voice Input";
            if (this.mode === "domain" && this.originalPlaceholder) {
                this.activeTarget.placeholder = this.originalPlaceholder;
            }
        }
        this.activeBtn = null;
        this.activeTarget = null;
    }
}

// Instantiate globally
window.omniVoice = new VoiceInputSystem();

document.addEventListener("DOMContentLoaded", () => {
    window.omniVoice.init();
});
