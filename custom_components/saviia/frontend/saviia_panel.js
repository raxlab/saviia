class SaviiaPanel extends HTMLElement {
    set hass(hass) {
        this._hass = hass;

        if (!this._loaded) {
            this._loaded = true;
            this._loadReact();
        } else if (this._update) {
            this._update(hass);
        }
    }

    async _loadReact() {
        try {
            const module = await import("./main.js");

            this._mount = module.updateApp;
            
            module.mountApp(this, this._hass)
        } catch (err) {
            console.error("Error loading React:", err);
        }
    }
}

customElements.define("saviia-panel", SaviiaPanel);
