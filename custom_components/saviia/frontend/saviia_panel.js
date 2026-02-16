class SaviiaPanel extends HTMLElement {
    set hass(hass) {
        this._hass = hass;
        this._load();
    }

    async _load() {
        if (!this._loaded) {
            const response = await fetch("/frontend/saviia/index.html");
            this.innerHTML = await response.text();

            window.hass = this._hass;

            await import("/frontend/saviia/js/new_task/new_task.js");

            this._loaded = true;
        }
    }
}

customElements.define("saviia-panel", SaviiaPanel);
