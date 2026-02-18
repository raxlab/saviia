import { createLogger } from './logger.js';

const logger = createLogger('HAClient');

class HAClient {
    constructor() {
        this.baseUrl = import.meta.env?.VITE_HA_URL ?? "";
        this.token = import.meta.env?.VITE_HA_TOKEN ?? "";
    }
}

let hass;
let environment;
let baseUrl;
let token;

if (window.hass) {
    hass = window.hass
    logger.info("Running in Production mode (Home Assistant)", hass);
    environment = "production";
} else {
    logger.info("Running in Development mode (Local)");
    environment = "development";
    baseUrl = import.meta.env?.VITE_HA_URL ?? "";
    token = import.meta.env?.VITE_HA_TOKEN ?? "";
}

export { hass, environment, baseUrl, token };
