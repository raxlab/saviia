class SaviiaPanel extends HTMLElement {
    async set hass(hass) {
        this._hass = hass;

        if (!this._loaded) {
            this._loaded = true;

            const module = await import("/frontend/saviia/main.js");

            this._mount = module.mountApp;

            this._mount(this, hass);
        } else if (this._mount) {
            this._mount(this, hass);
        }
    }
}

customElements.define("saviia-panel", SaviiaPanel);
