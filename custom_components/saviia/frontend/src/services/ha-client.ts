import { HAApiUrl, HAToken } from '../config/env.config'
declare global {
    interface Window {
        hass?: any; 
    }
}

class HAClient {
    private baseUrl: string;
    private token: string;

    constructor(baseUrl: string, token: string) {
        this.baseUrl = baseUrl;
        this.token = token;
    }

    async callService(domain: string, service: string, data: any = {}) {
        console.log(this.baseUrl)
        const response = await fetch(
            `${this.baseUrl}/${domain}/${service}?return_response`,
            {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${this.token}`,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            }
        );

        return await response.json();
    }
}

let hass: any;
if (window.hass) {
    hass = window.hass
    console.log("Running in Production mode (Home Assistant)", hass);
} else {

    hass = new HAClient(HAApiUrl, HAToken);
    console.log("Running in Development mode (Local)");
}

export { hass };