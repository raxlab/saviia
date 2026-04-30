import {
    LitElement,
    html,
    css,
} from "https://unpkg.com/lit-element@2.4.0/lit-element.js?module";

import { Styles } from "./styles/index.js";
import TasksAPI from "./endpoints/tasks.endpoints.js";
import { createLogger } from "./services/logger.js";

const logger = createLogger("SaviiaSensorStatus");

const CACHE_KEY = "saviia.sensor_status.cache.v1";
const CACHE_INVALIDATION_EVENT = "saviia-sensor-status:invalidate-cache";

class SaviiaSensorStatusPanel extends LitElement {
    static get properties() {
        return {
            hass: { type: Object },
            rows: { type: Array },
            isLoading: { type: Boolean },
            error: { type: String },
            lastUpdated: { type: String },
        };
    }

    static styles = [
        ...new Styles().getStyles(["general", "table"]),
        css`
            /* Mobile-only Home button */
            #ha-home-btn {
                display: none;
                position: fixed;
                bottom: 16px;
                right: 16px;
                z-index: 9999;
                background: #03a9f4;
                color: #fff;
                border: none;
                border-radius: 12px;
                width: 56px;
                height: 56px;
                padding: 6px;
                display: inline-flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                box-shadow: 0 2px 6px rgba(0,0,0,0.25);
                cursor: pointer;
            }

            #ha-home-btn .label {
                font-size: 11px;
                margin-top: 2px;
                line-height: 1;
            }

            @media (max-width: 767px) {
                #ha-home-btn { display: inline-flex; }
            }
        `,
    ];

    constructor() {
        super();
        this.rows = [];
        this.isLoading = true;
        this.error = "";
        this.lastUpdated = "";
        this.tasksAPI = null;
        this._initialized = false;
        this._reloadInvalidated = false;
        this._boundInvalidateListener = this.handleCacheInvalidationEvent.bind(this);
    }


    openHome() {
        var origin = window.location && window.location.origin;
        if (!origin || origin === "null") {
            origin = window.location.protocol + "//" + window.location.hostname + (window.location.port ? ":" + window.location.port : "");
        }
        window.location.href = origin + "/";
    }

    set hass(hass) {
        this._hass = hass;

        if (!this.tasksAPI || this.tasksAPI.hass !== hass) {
            this.tasksAPI = new TasksAPI(hass);
        }

        if (!this._initialized && hass) {
            this._initialized = true;
            this.fetchSensorsStatus();
        }
    }

    get hass() {
        return this._hass;
    }

    connectedCallback() {
        super.connectedCallback();
        this.invalidateCacheOnReload();
        window.addEventListener(CACHE_INVALIDATION_EVENT, this._boundInvalidateListener);

        // Dev mode only: allow standalone loading without Home Assistant on localhost:8000.
        if (!this._initialized && !this._hass && window.location.hostname === "localhost" && window.location.port === "8000") {
            this.tasksAPI = new TasksAPI();
            this._initialized = true;
            this.fetchSensorsStatus();
        }
    }

    disconnectedCallback() {
        super.disconnectedCallback();
        window.removeEventListener(CACHE_INVALIDATION_EVENT, this._boundInvalidateListener);
    }

    handleCacheInvalidationEvent() {
        this.clearCache();
        this.fetchSensorsStatus(true);
    }

    invalidateCacheOnReload() {
        if (this._reloadInvalidated) {
            return;
        }

        this._reloadInvalidated = true;

        let navigationType = "";
        try {
            const entries = performance.getEntriesByType("navigation");
            navigationType = entries[0]?.type || "";
        } catch (error) {
            logger.warn("Could not read navigation entries", error);
        }

        if (navigationType === "reload") {
            this.clearCache();
            logger.info("Cache invalidated due to page reload");
        }
    }

    clearCache() {
        localStorage.removeItem(CACHE_KEY);
    }

    readCache() {
        const rawCache = localStorage.getItem(CACHE_KEY);
        if (!rawCache) return null;

        try {
            const parsed = JSON.parse(rawCache);
            if (!Array.isArray(parsed?.rows)) {
                return null;
            }
            return parsed;
        } catch (error) {
            logger.warn("Invalid cache format. Clearing cache.", error);
            this.clearCache();
            return null;
        }
    }

    writeCache(rows, sourcePath) {
        const payload = {
            rows,
            sourcePath,
            days: 7,
            cachedAt: new Date().toISOString(),
        };
        localStorage.setItem(CACHE_KEY, JSON.stringify(payload));
    }

    extractValidationPayload(result) {
        if (result?.service_response?.api_metadata?.validation) {
            return result.service_response.api_metadata.validation;
        }

        if (result?.api_metadata?.validation) {
            return result.api_metadata.validation;
        }

        if (result?.validation) {
            return result.validation;
        }

        return result;
    }

    normalizeRows(validationBySensor) {
        if (!validationBySensor || typeof validationBySensor !== "object") {
            return [];
        }

        return Object.entries(validationBySensor).map(([sensorName, metadata]) => ({
            sensorName,
            sensorFailed: Boolean(metadata?.sensor_failed),
            consideredParam: metadata?.considered_param || "-",
            daysWithFailures: Number(metadata?.days_with_failures ?? 0),
            daysOutOfBound: Number(metadata?.days_out_of_bound ?? 0),
            daysAllZeros: Number(metadata?.days_all_zeros ?? 0),
        }));
    }

    async fetchSensorsStatus(forceRefresh = false) {
        this.isLoading = true;
        this.error = "";

        try {
            if (!forceRefresh) {
                const cached = this.readCache();
                if (cached) {
                    this.rows = cached.rows;
                    this.lastUpdated = cached.cachedAt;
                    this.isLoading = false;
                    logger.info("Using sensor status from cache", { rows: cached.rows.length });
                    return;
                }
            }

            const localBackupPath = await this.tasksAPI.getConfigFlowValue("local_backup_source_path");
            if (!localBackupPath) {
                throw new Error("No se encontro local_backup_source_path en la configuracion.");
            }

            const failedSensorsResult = await this.tasksAPI.getFailedSensors(localBackupPath, 7);
            const validation = this.extractValidationPayload(failedSensorsResult);
            const rows = this.normalizeRows(validation);

            this.rows = rows;
            this.lastUpdated = new Date().toISOString();
            this.writeCache(rows, localBackupPath);
            logger.info("Sensor status fetched and cached", { rows: rows.length });
        } catch (error) {
            logger.error("Error fetching sensor status", error);
            this.error = `Error cargando estado de sensores: ${error.message}`;
            this.rows = [];
        } finally {
            this.isLoading = false;
        }
    }


    formatTimestamp(isoDate) {
        if (!isoDate) return "-";

        const date = new Date(isoDate);
        if (Number.isNaN(date.getTime())) return "-";
        return date.toLocaleString("es-ES");
    }

    renderTable() {
        if (!this.rows.length) {
            return html`<div class="empty">No hay sensores para mostrar.</div>`;
        }

        return html`
            <div class="table-container">
                <table class="tasks-table" role="grid" aria-label="Estado de sensores">
                    <thead>
                        <tr>
                            <th>Sensor</th>
                            <th>Estado</th>
                            <th>Dias con fallas</th>
                            <th>Dias Fuera de Rango</th>
                            <th>Dias Todos Ceros</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${this.rows.map((row) => {
                            const statusClass = row.sensorFailed ? "failed" : "ok";
                            return html`
                                <tr>
                                    <td>
                                        <div class="sensor-name">${row.sensorName}</div>
                                        <small>${row.consideredParam}</small>
                                    </td>
                                    <td>
                                        <div class="status-cell">
                                            <span class="status-dot ${statusClass}" aria-hidden="true"></span>
                                            <span class="status-text ${statusClass}">
                                                ${row.sensorFailed ? "Failed" : "Healthy"}
                                            </span>
                                        </div>
                                    </td>
                                    <td>${row.daysWithFailures}</td>
                                    <td>${row.daysOutOfBound}</td>
                                    <td>${row.daysAllZeros}</td>
                                </tr>
                            `;
                        })}
                    </tbody>
                </table>
            </div>
        `;
    }

    render() {
        return html`
            <section class="header">
                <h2>Sensor Status</h2>
                <p>Últimos 7 días</p>
                <p class="help-text">
                    Panel de estado de sensores de la THIES Data Logger.
                </p>
                <p class="meta">Ultima actualizacion: ${this.formatTimestamp(this.lastUpdated)}</p>
            </section>

            ${this.isLoading ? html`<div class="loading-spinner">Cargando estado de sensores...</div>` : null}
            ${this.error ? html`<div class="error">${this.error}</div>` : null}
            ${!this.isLoading && !this.error ? this.renderTable() : null}
            <!-- Mobile-only Home button -->
            <button id="ha-home-btn" @click="${this.openHome}" aria-label="Open Home">
                <span class="icon" aria-hidden="true">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M3 10.5L12 4l9 6.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1V10.5z" fill="currentColor"/>
                    </svg>
                </span>
                <span class="label">Home</span>
            </button>
        `;
    }
}

customElements.define("saviia-sensor-status", SaviiaSensorStatusPanel);
