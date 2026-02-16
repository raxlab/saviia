class SaviiaPanel extends HTMLElement {
    async set hass(hass) {
        this._hass = hass;
        if (!this._loaded) {
            const response = await fetch("/frontend/saviia/index.html");
            this.innerHTML = await response.text();
            window.hass = hass;
            await import("/frontend/saviia/js/new_task/new_task.js");
            this._loaded = true;
        }
    }
}

customElements.define("saviia_panel", SaviiaPanel);
