class SaviiaPanel extends HTMLElement {
    set hass(hass) {
        this._hass = hass;

        if (!this._loaded) {
            this._loaded = true;
            this._loadReact();
        } else if (this._mount) {
            this._mount(this, hass);
        }
    }

    async _loadReact() {
        try {
            const module = await import("/frontend/saviia/main.js");

            this._mount = module.mountApp;

            if (this._mount) {
                this._mount(this, this._hass);
            }
        } catch (err) {
            console.error("Error loading React:", err);
        }
    }
}

customElements.define("saviia-panel", SaviiaPanel);
