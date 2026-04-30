import {
	LitElement,
	html,
	css,
} from "https://unpkg.com/lit-element@2.4.0/lit-element.js?module";

import "./saviia-get-tasks.panel.js";
import "./saviia-gantt.panel.js";
import "./saviia-create-task.panel.js";
import { createLogger } from "./services/logger.js";

const logger = createLogger("SaviiaTasksPanel");
logger.info("SAVIIA Combined Tasks panel loading...");

class SaviiaTasksPanel extends LitElement {
	static get properties() {
		return {
			hass: { type: Object },
			activeView: { type: String },
		};
	}

	static styles = css`
		:host {
			display: block;
			box-sizing: border-box;
			padding: 0.6rem;
		}

		.panel-wrapper {
			max-width: 100%;
			margin: 0 auto;
		}

		.view-switch {
			display: inline-flex;
			gap: 0.4rem;
			padding: 0.25rem;
			border-radius: 12px;
			border: 1px solid #d5dde4;
			background: #f4f7fa;
			margin-bottom: 0.75rem;
		}

		.view-btn {
			border: none;
			border-radius: 10px;
			padding: 0.5rem 0.8rem;
			background: transparent;
			color: #425463;
			font-weight: 600;
			font-size: 0.9rem;
			cursor: pointer;
			transition: background 0.15s ease, color 0.15s ease, box-shadow 0.15s ease;
		}

		.view-btn:hover {
			background: #e8eef4;
		}

		.view-btn.active {
			background: #ffffff;
			color: #1d425f;
			box-shadow: 0 2px 8px rgba(38, 58, 77, 0.12);
		}

		.view-panel {
			display: block;
		}

		.view-panel[hidden] {
			display: none;
		}

		@media (max-width: 768px) {
			:host {
				padding: 0.35rem;
			}

			.view-switch {
				display: grid;
				grid-template-columns: 1fr 1fr 1fr;
				width: 100%;
			}

			.view-btn {
				width: 100%;
				font-size: 0.85rem;
				padding: 0.5rem 0.6rem;
			}
		}

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
	`;

	constructor() {
		super();
		this.activeView = "checklist";
		this.hass = null;
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
		this.requestUpdate();
	}

	get hass() {
		return this._hass;
	}

	updated() {
		this.syncChildHass();
	}

	syncChildHass() {
		if (!this._hass) return;

		const checklist = this.shadowRoot?.querySelector("saviia-get-tasks");
		const gantt = this.shadowRoot?.querySelector("saviia-gantt");
		const createTask = this.shadowRoot?.querySelector("saviia-create-task");

		if (checklist && checklist.hass !== this._hass) {
			checklist.hass = this._hass;
		}

		if (gantt && gantt.hass !== this._hass) {
			gantt.hass = this._hass;
		}

		if (createTask && createTask.hass !== this._hass) {
			createTask.hass = this._hass;
		}
	}

	handleViewChange(view) {
		this.activeView = view;
	}

	render() {
		const isChecklist = this.activeView === "checklist";
		const isGantt = this.activeView === "gantt";
		const isCreate = this.activeView === "create";

		return html`
			<div class="panel-wrapper">
				<div class="view-switch" role="tablist" aria-label="Cambiar vista de tareas">
					<button
						class="view-btn ${isChecklist ? "active" : ""}"
						role="tab"
						aria-selected=${isChecklist ? "true" : "false"}
						@click=${() => this.handleViewChange("checklist")}
					>
						Checklist
					</button>
					<button
						class="view-btn ${isGantt ? "active" : ""}"
						role="tab"
						aria-selected=${isGantt ? "true" : "false"}
						@click=${() => this.handleViewChange("gantt")}
					>
						Gantt
					</button>
					<button
						class="view-btn ${isCreate ? "active" : ""}"
						role="tab"
						aria-selected=${isCreate ? "true" : "false"}
						@click=${() => this.handleViewChange("create")}
					>
						Crear
					</button>
				</div>

				<section class="view-panel" ?hidden=${!isChecklist}>
					<saviia-get-tasks></saviia-get-tasks>
				</section>

				<section class="view-panel" ?hidden=${!isGantt}>
					<saviia-gantt></saviia-gantt>
				</section>

				<section class="view-panel" ?hidden=${!isCreate}>
					<saviia-create-task></saviia-create-task>
				</section>
			</div>

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

customElements.define("saviia-tasks", SaviiaTasksPanel);
