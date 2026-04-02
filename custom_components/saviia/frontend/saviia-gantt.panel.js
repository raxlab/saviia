import {
    LitElement,
    html,
    css,
} from "https://unpkg.com/lit-element@2.4.0/lit-element.js?module";

import { Styles } from "./styles/index.js";
import TasksAPI from "./endpoints/tasks.endpoints.js";
import { createLogger } from "./services/logger.js";

const logger = createLogger("SaviiaGanttPanel");

class SaviiaGanttPanel extends LitElement {
    static get properties() {
        return {
            hass: { type: Object },
            tasks: { type: Array },
            isLoading: { type: Boolean },
            error: { type: String },
            windowStart: { type: String },
            hoverInfo: { type: Object },
        };
    }

    static styles = new Styles().getStyles(['general', 'gantt']);

    constructor() {
        super();
        const now = new Date();
        const year = now.getFullYear();
        this.tasks = [];
        this.isLoading = true;
        this.error = "";
        this.windowStart = `${year}-01-01`;
        this.hoverInfo = null;
        this.tasksAPI = null;
        this._initialized = false;
    }

    set hass(hass) {
        this._hass = hass;

        if (!this.tasksAPI || this.tasksAPI.hass !== hass) {
            this.tasksAPI = new TasksAPI(hass);
        }

        if (!this._initialized && hass) {
            this._initialized = true;
            this.fetchTasks();
        }
    }

    connectedCallback() {
        super.connectedCallback();
        if (!this._initialized && !this._hass && window.location.hostname === "localhost" && window.location.port === "8000") {
            this.tasksAPI = new TasksAPI();
            this._initialized = true;
            this.fetchTasks();
        }
    }

    parseDate(dateLike) {
        if (!dateLike || typeof dateLike !== "string") return null;
        const m = dateLike.match(/^(\d{4})-(\d{2})-(\d{2})$/);
        if (!m) return null;

        const year = Number(m[1]);
        const month = Number(m[2]) - 1;
        const day = Number(m[3]);
        const d = new Date(year, month, day);

        if (
            Number.isNaN(d.getTime()) ||
            d.getFullYear() !== year ||
            d.getMonth() !== month ||
            d.getDate() !== day
        ) {
            return null;
        }

        return d;
    }

    toIsoDate(dateObj) {
        const y = dateObj.getFullYear();
        const m = String(dateObj.getMonth() + 1).padStart(2, "0");
        const d = String(dateObj.getDate()).padStart(2, "0");
        return `${y}-${m}-${d}`;
    }

    addMonths(dateObj, months) {
        const d = new Date(dateObj);
        d.setMonth(d.getMonth() + months);
        d.setDate(1);
        return d;
    }

    monthKey(dateObj) {
        return dateObj.getFullYear() * 12 + dateObj.getMonth();
    }

    sameMonth(a, b) {
        return a && b && a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth();
    }

    isCurrentMonth(dateObj) {
        const now = new Date();
        return dateObj.getFullYear() === now.getFullYear() && dateObj.getMonth() === now.getMonth();
    }

    normalizeTask(task) {
        const creation = this.parseDate(task.creation);
        const deadline = this.parseDate(task.deadline);

        if (!creation && !deadline) {
            return null;
        }

        let start = creation || deadline;
        let end = deadline || creation;

        if (start > end) {
            const tmp = start;
            start = end;
            end = tmp;
        }

        const execution = this.parseDate(task.execution);

        return {
            title: task.title || "(Sin titulo)",
            start,
            end,
            execution,
            completed: Boolean(task.completed),
            priority: task.priority,
            description: task.description,
            category: task.category,
            assignee: task.assignee,
            taskId: task.task_id,
        };
    }

    getWindowStart() {
        const parsed = this.parseDate(this.windowStart);
        if (!parsed) {
            const now = new Date();
            return new Date(now.getFullYear(), 0, 1);
        }
        return new Date(parsed.getFullYear(), parsed.getMonth(), 1);
    }

    getWindowMonths() {
        const start = this.getWindowStart();
        return Array.from({ length: 12 }, (_, index) => this.addMonths(start, index));
    }

    getWindowBounds() {
        const months = this.getWindowMonths();
        return {
            startMonth: months[0],
            endMonth: months[months.length - 1],
            months,
        };
    }

    taskIntersectsWindow(task, startMonth, endMonth) {
        const taskStartKey = this.monthKey(task.start);
        const taskEndKey = this.monthKey(task.end);
        const startKey = this.monthKey(startMonth);
        const endKey = this.monthKey(endMonth);
        return taskStartKey <= endKey && taskEndKey >= startKey;
    }

    getVisibleTasks() {
        const { startMonth, endMonth } = this.getWindowBounds();
        const normalized = this.tasks
            .map((task) => this.normalizeTask(task))
            .filter((task) => task && this.taskIntersectsWindow(task, startMonth, endMonth));

        normalized.sort((a, b) => a.start - b.start);
        return normalized;
    }

    isTaskActiveInMonth(task, monthDate) {
        const mKey = this.monthKey(monthDate);
        return mKey >= this.monthKey(task.start) && mKey <= this.monthKey(task.end);
    }

    formatDate(dateObj) {
        if (!(dateObj instanceof Date) || Number.isNaN(dateObj.getTime())) return "-";
        const options = { year: "numeric", month: "short", day: "2-digit" };
        return dateObj.toLocaleDateString("es-ES", options);
    }

    async fetchTasks() {
        this.isLoading = true;
        this.error = "";

        try {
            const tasks = await this.tasksAPI.getTasks();
            this.tasks = Array.isArray(tasks) ? tasks : [];
            logger.info("Tasks loaded for timeline", { count: this.tasks.length });
        } catch (error) {
            logger.error("Error loading tasks for timeline", error);
            this.error = `Error cargando tareas: ${error.message}`;
            this.tasks = [];
        } finally {
            this.isLoading = false;
        }
    }

    handleShiftWindow(direction) {
        const start = this.getWindowStart();
        const shift = direction === "next" ? 1 : -1;
        this.windowStart = this.toIsoDate(this.addMonths(start, shift));
    }

    handleResetYear() {
        const year = new Date().getFullYear();
        this.windowStart = `${year}-01-01`;
    }

    handleCellHover(event, task) {
        this.hoverInfo = {
            x: event.clientX + 12,
            y: event.clientY + 12,
            title: task.title,
            creation: this.formatDate(task.start),
            deadline: this.formatDate(task.end),
            execution: task.completed ? this.formatDate(task.execution) : "-",
        };
    }

    handleCellLeave() {
        this.hoverInfo = null;
    }

    renderTooltip() {
        if (!this.hoverInfo) return null;

        return html`
      <div class="tooltip" style="left:${this.hoverInfo.x}px; top:${this.hoverInfo.y}px;">
        <strong>${this.hoverInfo.title}</strong><br />
        Fecha de creación: ${this.hoverInfo.creation}<br />
        Fecha de ejecución: ${this.hoverInfo.execution}<br />
        Fecha límite: ${this.hoverInfo.deadline}
      </div>
    `;
    }

    renderChart() {
        const { months } = this.getWindowBounds();
        const visibleTasks = this.getVisibleTasks();

        if (visibleTasks.length === 0) {
            return html`<div class="empty">No hay tareas en esta ventana de 12 meses.</div>`;
        }

        return html`
      <div class="chart-shell">
        <div class="chart-scroll">
          <table class="month-grid" role="grid" aria-label="Gantt mensual de tareas">
            <thead>
              <tr>
                <th class="task-col">Tarea</th>
                ${months.map(
            (monthDate) =>
                html`<th class="month-head ${this.isCurrentMonth(monthDate) ? 'month-head-current' : ''}">${(() => {
                    const monthLabel = monthDate.toLocaleDateString("es-ES", {
                        month: "short",
                    }).toLocaleUpperCase();

                    return monthDate.getMonth() === 0
                        ? `${monthLabel} - ${monthDate.getFullYear()}`
                        : monthLabel;
                })()}</th>`
        )}
              </tr>
            </thead>
            <tbody>
              ${visibleTasks.map((task) => {
            return html`
                  <tr>
                                        <th class="task-col" title=${task.title} aria-label=${task.title}>
                                            <span class="task-title-text">${task.title}</span>
                                        </th>
                    ${months.map((monthDate) => {
                const isActive = this.isTaskActiveInMonth(task, monthDate);
                const hasExecutionMarker = task.completed && this.sameMonth(task.execution, monthDate);
                const cellClass = [
                    "cell-wrap",
                    isActive ? "cell-active" : "",
                    isActive && !task.completed ? "cell-pending" : "",
                    isActive && task.completed ? "cell-completed" : "",
                ]
                    .filter(Boolean)
                    .join(" ");

                return html`
                                                <td class="${this.isCurrentMonth(monthDate) ? 'month-col-current' : ''}">
                          <span
                            class="${cellClass}"
                            @mouseenter=${isActive ? (e) => this.handleCellHover(e, task) : null}
                            @mousemove=${isActive ? (e) => this.handleCellHover(e, task) : null}
                                                        @click=${isActive ? (e) => this.handleCellHover(e, task) : null}
                            @mouseleave=${isActive ? this.handleCellLeave : null}
                          >
                            ${hasExecutionMarker ? html`<span class="cell-check">✔</span>` : null}
                          </span>
                        </td>
                      `;
            })}
                  </tr>
                `;
        })}
            </tbody>
          </table>
        </div>
      </div>
    `;
    }

    render() {
        const months = this.getWindowMonths();
        const windowLabel = `${months[0].toLocaleDateString("es-ES", {
            month: "long",
            year: "numeric",
        })} - ${months[11].toLocaleDateString("es-ES", { month: "long", year: "numeric" })}`;

        return html`
      <div class="panel">
        <h2>Diagrama de Gantt de Saviia Tasks</h2>
        <p>
            Este panel muestra una vista de 12 meses de tus tareas en Saviia. 
            Las tareas se representan como barras que abarcan desde su fecha de creación hasta su fecha límite.
            Las tareas completadas se muestran en verde, mientras que las pendientes se muestran en rojo. 
            Un marcador "✔" indica el mes en que se ejecutó la tarea. Usa los botones para navegar entre ventanas de 12 meses o para volver al año actual.
        </p>
        <p class="window-caption">Ventana actual: ${windowLabel}</p>

        <div class="toolbar">
          <div class="button-row">
            <button @click=${() => this.handleShiftWindow("prev")}>Mes anterior</button>
            <button @click=${() => this.handleShiftWindow("next")}>Mes siguiente</button>
            <button @click=${this.handleResetYear}>Mes actual</button>
            <button @click=${() => this.fetchTasks()}>Recargar</button>
          </div>
        </div>

        <div class="legend">
          <span class="legend-item"><span class="square-swatch" style="background:#e53935"></span>Pendiente</span>
          <span class="legend-item"><span class="square-swatch" style="background:#43a047"></span>Completada</span>
          <span class="legend-item">✔ = mes de ejecucion</span>
        </div>

        ${this.isLoading ? html`<div class="empty">Cargando tareas...</div>` : null}
        ${this.error ? html`<div class="error">${this.error}</div>` : null}
        ${!this.isLoading && !this.error ? this.renderChart() : null}
      </div>
      ${this.renderTooltip()}
    `;
    }
}

customElements.define("saviia-gantt", SaviiaGanttPanel);
