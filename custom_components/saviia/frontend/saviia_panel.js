class SaviiaPanel extends HTMLElement {
    set hass(hass) {
        this._hass = hass;

        if (!this._loaded) {
            this._loaded = true;

            // const module = import("/frontend/saviia/main.js");
            const module = import("http://localhost:5173/src/main.jsx");

            this._mount = module.mountApp;

            this._mount(this, hass);
        } else if (this._mount) {
            this._mount(this, hass);
        }
    }
}

customElements.define("saviia-panel", SaviiaPanel);
