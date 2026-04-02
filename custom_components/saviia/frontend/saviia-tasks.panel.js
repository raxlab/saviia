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
	`;

	constructor() {
		super();
		this.activeView = "checklist";
		this.hass = null;
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
		`;
	}
}

customElements.define("saviia-tasks", SaviiaTasksPanel);
