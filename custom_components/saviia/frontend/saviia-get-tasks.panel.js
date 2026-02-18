import {
    LitElement,
    html,
} from "https://unpkg.com/lit-element@2.4.0/lit-element.js?module";

import { Styles } from './styles/index.js';
import TasksAPI from './endpoints/tasks.endpoints.js';
import { createLogger } from './services/logger.js';

const logger = createLogger('SaviiaGetTasks');
logger.info("SAVIIA Get Tasks panel loading...");

class SaviiaGetTasks extends LitElement {
    set hass(hass) {
        this._hass = hass;
        if (!this.tasksAPI) {
            this.tasksAPI = new TasksAPI(hass);
        } 
    }
    static get properties() {
        return {
            hass: { type: Object },
            allTasks: { type: Array },
            filteredTasks: { type: Array },
            isLoading: { type: Boolean },
            error: { type: String },
            filterStatus: { type: String },
            filterPriority: { type: String },
            filterDateFrom: { type: String },
            filterDateTo: { type: String },
            sortBy: { type: String },
            showFilters: { type: Boolean },
            isSubmitting: { type: Boolean },
            selectedTask: { type: Object },
            modalEmbeds: { type: Array },
            isModalOpen: { type: Boolean },
            isEditing: { type: Boolean },
            deleteConfirmText: { type: String },
            tasksAPI: { type: Object },
        };
    }

    static styles = new Styles().getStyles(['general', 'form', 'alert', 'modal', 'table']);

    constructor() {
        super();
        this.allTasks = [];
        this.filteredTasks = [];
        this.isLoading = true;
        this.error = '';
        this.filterStatus = '';
        this.filterPriority = '';
        this.filterDateFrom = '';
        this.filterDateTo = '';
        this.sortBy = '';
        this.showFilters = false;
        this.isSubmitting = false;
        this.selectedTask = null;
        this.modalEmbeds = [];
        this.isModalOpen = false;
        this.isEditing = false;
        this.deleteConfirmText = '';
        this.CONFIG = {
            ALERT_TIMEOUT: 3000,
            DELETE_CONFIRM_TEXT: 'delete-task',
        };
    }

    connectedCallback() {
        super.connectedCallback();
        this.fetchTasks();
    }

    disconnectedCallback() {
        super.disconnectedCallback();
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    parsePeriodicity(periodicityStr) {
        if (!periodicityStr || periodicityStr === "Sin periodicidad") {
            return { type: "", number: "" };
        }
        const match = periodicityStr.match(/Cada (\d+) (día|semana|mes|año)\(s\)/);
        if (match) {
            const number = match[1];
            const unit = match[2];
            const typeMap = {
                'día': 'daily',
                'semana': 'weekly',
                'mes': 'monthly',
                'año': 'yearly'
            };
            return {
                type: typeMap[unit] || "",
                number: number
            };
        }
        return { type: "", number: "" };
    }

    getPeriodicity(periodicity, periodicityNum) {
        if (periodicity === "" || periodicity === "Sin periodicidad")
            return "Sin periodicidad";
        else if (periodicity === "daily")
            return `Cada ${periodicityNum} día(s)`;
        else if (periodicity === "weekly")
            return `Cada ${periodicityNum} semana(s)`;
        else if (periodicity === "monthly")
            return `Cada ${periodicityNum} mes(es)`;
        else if (periodicity === "yearly")
            return `Cada ${periodicityNum} año(s)`;
        return "Sin periodicidad";
    }

    parseTaskContent(content) {
        const lines = content.split('\n').filter(line => line.trim());
        const task = {
            title: '',
            deadline: '',
            description: '',
            periodicity: '',
            priority: '',
            category: '',
            assignee: '',
            status: '',
        };

        lines.forEach(line => {
            if (line.startsWith('##')) {
                task.title = line.replace('##', '').trim();
            } else if (line.includes('__Fecha de realización__')) {
                task.deadline = line.split(':')[1]?.trim() || '';
            } else if (line.includes('__Descripcion__')) {
                task.description = line.split(':')[1]?.trim() || '';
            } else if (line.includes('__Periodicidad__')) {
                task.periodicity = line.split(':')[1]?.trim() || '';
            } else if (line.includes('__Prioridad__')) {
                task.priority = line.split(':')[1]?.trim() || '';
            } else if (line.includes('__Categoría__')) {
                task.category = line.split(':')[1]?.trim() || '';
            } else if (line.includes('__Persona asignada__')) {
                task.assignee = line.split(':')[1]?.trim() || '';
            } else if (line.includes('__Estado__')) {
                task.status = line.split(':')[1]?.trim() || '';
            }
        });

        return task;
    }

    sortTasks(tasks, sortType) {
        const sorted = [...tasks];
        switch (sortType) {
            case 'date-asc':
                sorted.sort((a, b) => new Date(a.deadline) - new Date(b.deadline));
                break;
            case 'date-desc':
                sorted.sort((a, b) => new Date(b.deadline) - new Date(a.deadline));
                break;
            case 'priority-asc':
                sorted.sort((a, b) => parseInt(a.priority) - parseInt(b.priority));
                break;
            case 'priority-desc':
                sorted.sort((a, b) => parseInt(b.priority) - parseInt(a.priority));
                break;
        }
        return sorted;
    }

    filterTasks(tasks, filters) {
        let filtered = [...tasks];
        if (filters.status) {
            filtered = filtered.filter(task => task.status === filters.status);
        }
        if (filters.priority) {
            filtered = filtered.filter(task => task.priority === filters.priority);
        }
        if (filters.dateFrom || filters.dateTo) {
            filtered = filtered.filter(task => {
                const taskDate = new Date(task.deadline);
                if (filters.dateFrom) {
                    const fromDate = new Date(filters.dateFrom);
                    if (taskDate < fromDate) return false;
                }
                if (filters.dateTo) {
                    const toDate = new Date(filters.dateTo);
                    if (taskDate > toDate) return false;
                }
                return true;
            });
        }
        return filtered;
    }
    // API calls
    async fetchTasks() {
        try {
            const messages = await this.tasksAPI.getTasks();
            logger.debug("Fetched messages:", messages);
            if (!Array.isArray(messages) || messages.length === 0) {
                this.error = "No hay tareas creadas aún.";
                this.isLoading = false;
                alert("No hay tareas creadas aún.");
                return;
            }
            const tasks = messages
                .filter(msg => msg.content && msg.content.trim().length > 0)
                .map(msg => ({
                    ...this.parseTaskContent(msg.content),
                    messageId: msg.id,
                    channelId: msg.channel_id,
                    createdAt: new Date(msg.timestamp).toLocaleDateString('es-ES'),
                    embeds: msg.embeds || []
                }));
            localStorage.setItem('tasksCache', JSON.stringify(tasks));
            if (tasks.length === 0) {
                this.error = "No hay tareas para mostrar.";
                this.isLoading = false;
                alert("No hay tareas para mostrar.");
                return;
            }
            this.allTasks = tasks;
            this.filterAndSortTasks();
            this.isLoading = false;

        } catch (error) {
            logger.error("Error fetching tasks:", error);
            this.error = `Error: ${error.message}`;
            this.isLoading = false;
            alert(error.message);
        }
    }

    async updateTask(task, completed) {
        const response = await this.tasksAPI.updateTask(task, completed)
        const status = response.service_response.api_status;
        if (status !== 200) {
            const error_msg = response.service_response.api_metadata.error;
            throw new Error(`Error al actualizar la tarea: ${error_msg}`);
        }
        return response.service_response.metadata;
    }

    async deleteTask(taskId) {
        const response = await this.tasksAPI.deleteTask(taskId)
        const status = response.service_response.api_status;
        if (status !== 200) {
            const error_msg = response.service_response.api_metadata.error;
            throw new Error(`Error al eliminar la tarea: ${error_msg}`);
        }
        return response;
    }
    // Event handlers
    filterAndSortTasks() {
        let filtered = this.filterTasks(this.allTasks, {
            status: this.filterStatus,
            priority: this.filterPriority,
            dateFrom: this.filterDateFrom,
            dateTo: this.filterDateTo
        });
        if (this.sortBy) {
            filtered = this.sortTasks(filtered, this.sortBy);
        }
        this.filteredTasks = filtered;
    }

    handleFilterChange() {
        this.filterAndSortTasks();
    }

    handleClearFilters() {
        this.filterStatus = '';
        this.filterPriority = '';
        this.filterDateFrom = '';
        this.filterDateTo = '';
        this.sortBy = '';
        this.filterAndSortTasks();
    }

    handleToggleFilters() {
        this.showFilters = !this.showFilters;
    }

    handleReload() {
        location.reload();
    }

    handleOpenModal(task, embeds) {
        this.selectedTask = task;
        this.modalEmbeds = embeds;
        this.isModalOpen = true;
        this.isEditing = false;
        this.deleteConfirmText = '';
    }

    handleCloseModal() {
        this.isModalOpen = false;
        this.isEditing = false;
        this.selectedTask = null;
        this.deleteConfirmText = '';
    }

    handleEditClick() {
        this.isEditing = true;
    }

    handleCancelEdit() {
        this.isEditing = false;
    }

    handleDeleteClick() {
        const deleteModal = this.shadowRoot?.querySelector('.delete-confirm-modal');
        if (deleteModal) {
            deleteModal.classList.add('show');
        }
    }

    handleDeleteInput(e) {
        this.deleteConfirmText = e.target.value;
    }

    handleDeleteConfirm() {
        if (this.selectedTask) {
            this.handleDeleteTask(this.selectedTask);
        }
    }

    handleFormSubmit(e) {
        e.preventDefault();
        if (!this.selectedTask) return;

        const form = e.target;
        const formData = new FormData(form);
        this.handleSubmitEdit(this.selectedTask, formData);
    }

    handleModalClickOutside(e) {
        if (e.target === this.shadowRoot.querySelector('.task-modal')) {
            this.handleCloseModal();
        }
    }

    async handleSubmitEdit(task, formData) {
        try {
            const newStatus = formData.get('status');
            const completed = newStatus === "Completada";
            const periodicity = formData.get('periodicity');
            const periodicityNum = formData.get('periodicity-number') || "1";
            const formattedPeriodicity = this.getPeriodicity(periodicity, periodicityNum);

            const updatedTask = {
                tid: task.messageId,
                title: formData.get('title'),
                deadline: formData.get('deadline'),
                description: formData.get('description'),
                periodicity: formattedPeriodicity,
                priority: parseInt(formData.get('priority')),
                category: formData.get('category'),
                assignee: formData.get('assignee'),
                status: newStatus,
            };

            await this.updateTask(updatedTask, completed);
            const tasksCache = JSON.parse(localStorage.getItem('tasksCache') || '[]');
            const updatedTasks = tasksCache.map(t =>
                t.messageId === task.messageId ? { ...t, ...updatedTask } : t
            );
            localStorage.setItem('tasksCache', JSON.stringify(updatedTasks));
            this.allTasks = updatedTasks;
            this.filterAndSortTasks();
            alert("Tarea actualizada exitosamente");
            this.handleCloseModal();
        } catch (error) {
            logger.error("Error updating task:", error);
            alert(`Error al actualizar: ${error.message}`);
        }
    }

    async handleDeleteTask(task) {
        try {
            logger.info('Deleting task:', task);
            await this.deleteTask(task.messageId);
            const tasksCache = JSON.parse(localStorage.getItem('tasksCache') || '[]');
            const updatedTasks = tasksCache.filter(t => t.messageId !== task.messageId);
            this.allTasks = updatedTasks;
            localStorage.setItem('tasksCache', JSON.stringify(updatedTasks));
            this.filterAndSortTasks();
            alert("Tarea eliminada exitosamente ✅");
            this.handleCloseModal();

            // Close the delete modal
            const deleteModal = this.shadowRoot?.querySelector('.delete-confirm-modal');
            if (deleteModal) {
                deleteModal.classList.remove('show');
            }
        } catch (error) {
            logger.error("Error deleting task:", error);
            alert(`Error al eliminar: ${error.message}`);
        }
    }

    handleDetailsClick(task) {
        this.handleOpenModal(task, task.embeds);
    }

    renderModalViewMode() {
        if (!this.selectedTask) return html``;
        return html`
            <h2 class="modal-task-title">${this.escapeHtml(this.selectedTask.title)}</h2>
            <div class="modal-task-field">
                <label class="modal-task-field-label">Fecha de realización</label>
                <div class="modal-task-field-value">${this.escapeHtml(this.selectedTask.deadline)}</div>
            </div>
            <div class="modal-task-field">
                <label class="modal-task-field-label">Estado</label>
                <div class="modal-task-field-value">${this.escapeHtml(this.selectedTask.status)}</div>
            </div>
            <div class="modal-task-field">
                <label class="modal-task-field-label">Prioridad</label>
                <div class="modal-task-field-value">
                    <span class="priority-badge priority-${this.selectedTask.priority}">${this.escapeHtml(this.selectedTask.priority)}</span>
                </div>
            </div>
            <div class="modal-task-field">
                <label class="modal-task-field-label">Categoría</label>
                <div class="modal-task-field-value">${this.escapeHtml(this.selectedTask.category)}</div>
            </div>
            <div class="modal-task-field">
                <label class="modal-task-field-label">Asignada a</label>
                <div class="modal-task-field-value">${this.escapeHtml(this.selectedTask.assignee)}</div>
            </div>
            <div class="modal-task-field">
                <label class="modal-task-field-label">Periodicidad</label>
                <div class="modal-task-field-value">${this.escapeHtml(this.selectedTask.periodicity)}</div>
            </div>
            <div class="modal-task-field">
                <label class="modal-task-field-label">Descripción</label>
                <div class="modal-task-field-value">${this.escapeHtml(this.selectedTask.description)}</div>
            </div>
            ${this.modalEmbeds && this.modalEmbeds.length > 0 ? html`
                <div class="modal-task-images">
                    <h3 class="modal-task-images-title">Imágenes adjuntas</h3>
                    ${this.modalEmbeds.map((embed, index) => html`
                        <div class="modal-task-image">
                            <img src="${embed.image?.url || ''}" alt="Task image ${index + 1}">
                            ${embed.title ? html`<div class="modal-task-image-caption">${this.escapeHtml(embed.title)}</div>` : ''}
                        </div>
                    `)}
                </div>
            ` : ''}
            <div class="modal-task-actions">
                <button class="modal-action-btn edit-btn" @click=${this.handleEditClick}>Editar</button>
            </div>
        `;
    }

    renderModalEditMode() {
        if (!this.selectedTask) return html``;
        return html`
            <h2 class="modal-task-title">Editar Tarea</h2>
            <form @submit=${this.handleFormSubmit}>
                <div class="modal-task-field">
                    <label class="modal-task-field-label" for="edit-title">Título</label>
                    <input type="text" id="edit-title" name="title" value="${this.escapeHtml(this.selectedTask.title)}" required>
                </div>
                <div class="modal-task-field">
                    <label class="modal-task-field-label" for="edit-status">Estado</label>
                    <select id="edit-status" name="status" required>
                        <option value="Pendiente" ?selected=${this.selectedTask.status === "Pendiente"}>Pendiente</option>
                        <option value="Completada" ?selected=${this.selectedTask.status === "Completada"}>Completada</option>
                    </select>
                </div>
                <div class="modal-task-field">
                    <label class="modal-task-field-label" for="edit-deadline">Fecha de realización</label>
                    <input type="date" id="edit-deadline" name="deadline" value="${this.selectedTask.deadline}" required>
                </div>
                <div class="modal-task-field">
                    <label class="modal-task-field-label" for="edit-priority">Prioridad</label>
                    <select id="edit-priority" name="priority" required>
                        <option value="1" ?selected=${this.selectedTask.priority == "1"}>1</option>
                        <option value="2" ?selected=${this.selectedTask.priority == "2"}>2</option>
                        <option value="3" ?selected=${this.selectedTask.priority == "3"}>3</option>
                        <option value="4" ?selected=${this.selectedTask.priority == "4"}>4</option>
                    </select>
                </div>
                <div class="modal-task-field">
                    <label class="modal-task-field-label" for="edit-category">Categoría</label>
                    <input type="text" id="edit-category" name="category" value="${this.escapeHtml(this.selectedTask.category)}">
                </div>
                <div class="modal-task-field">
                    <label class="modal-task-field-label" for="edit-assignee">Asignada a</label>
                    <input type="text" id="edit-assignee" name="assignee" value="${this.escapeHtml(this.selectedTask.assignee)}">
                </div>
                <div class="modal-task-field">
                    <label class="modal-task-field-label" for="edit-periodicity">Periodicidad</label>
                    <select id="edit-periodicity" name="periodicity">
                        <option value="" ?selected=${this.parsePeriodicity(this.selectedTask.periodicity).type === ""}>Sin periodicidad</option>
                        <option value="daily" ?selected=${this.parsePeriodicity(this.selectedTask.periodicity).type === "daily"}>Diaria</option>
                        <option value="weekly" ?selected=${this.parsePeriodicity(this.selectedTask.periodicity).type === "weekly"}>Semanal</option>
                        <option value="monthly" ?selected=${this.parsePeriodicity(this.selectedTask.periodicity).type === "monthly"}>Mensual</option>
                        <option value="yearly" ?selected=${this.parsePeriodicity(this.selectedTask.periodicity).type === "yearly"}>Anual</option>
                    </select>
                </div>
                <div class="modal-task-field">
                    <label class="modal-task-field-label" for="edit-periodicity-number">Número de Periodicidad</label>
                    <input type="number" id="edit-periodicity-number" name="periodicity-number" min="1" value="${this.parsePeriodicity(this.selectedTask.periodicity).number || ''}" placeholder="Ej: 2">
                </div>
                <div class="modal-task-field">
                    <label class="modal-task-field-label" for="edit-description">Descripción</label>
                    <textarea id="edit-description" name="description" rows="4">${this.escapeHtml(this.selectedTask.description)}</textarea>
                </div>
                <div class="modal-task-actions">
                    <button type="submit" class="modal-action-btn submit-btn">Guardar Cambios</button>
                    <button type="button" class="modal-action-btn cancel-btn" @click=${this.handleCancelEdit}>Cancelar cambios</button>
                    <button type="button" class="modal-action-btn delete-btn" @click=${this.handleDeleteClick}>Eliminar Tarea</button>
                </div>
            </form>
        `;
    }

    render() {
        return html`
      <div class="container">
        <h1>Lista de tareas</h1>
        <p>Checklist de tareas necesarias a realizar en la estación</p>
        
        <div class="header-actions">
          <button class="header-action-btn" @click=${this.handleToggleFilters}>
            ${this.showFilters ? 'Ocultar Filtros' : 'Mostrar Filtros'}
          </button>
          <button class="header-action-btn" @click=${this.handleReload}>
            Recargar
          </button>
        </div>

        ${this.isLoading ? html`<div class="loading-spinner show">Cargando tareas...</div>` : ''}

        ${this.error ? html`
          <div class="error-container">
            ${this.error}
          </div>
        ` : ''}
        ${this.showFilters ? html`
            <div class="filters-sort-container">
              <div class="filters-group">
                <label for="filter-status">Estado:</label>
                <select 
                  id="filter-status" 
                  .value=${this.filterStatus}
                  @change=${(e) => {
                    this.filterStatus = e.target.value;
                    this.handleFilterChange();
                }}
                >
                  <option value="">Todos</option>
                  <option value="Pendiente">Pendiente</option>
                  <option value="Completada">Completada</option>
                </select>
    
                <label for="filter-priority">Prioridad:</label>
                <select 
                  id="filter-priority"
                  .value=${this.filterPriority}
                  @change=${(e) => {
                    this.filterPriority = e.target.value;
                    this.handleFilterChange();
                }}
                >
                  <option value="">Todas</option>
                  <option value="1">1 - Crítica</option>
                  <option value="2">2 - Alta</option>
                  <option value="3">3 - Media</option>
                  <option value="4">4 - Baja</option>
                </select>
    
                <label for="filter-date-from">Desde:</label>
                <input 
                  type="date" 
                  id="filter-date-from"
                  .value=${this.filterDateFrom}
                  @change=${(e) => {
                    this.filterDateFrom = e.target.value;
                    this.handleFilterChange();
                }}
                />
    
                <label for="filter-date-to">Hasta:</label>
                <input 
                  type="date" 
                  id="filter-date-to"
                  .value=${this.filterDateTo}
                  @change=${(e) => {
                    this.filterDateTo = e.target.value;
                    this.handleFilterChange();
                }}
                />
              </div>
    
              <div class="sort-group">
                <label for="sort-by">Ordenar por:</label>
                <select 
                  id="sort-by"
                  .value=${this.sortBy}
                  @change=${(e) => {
                    this.sortBy = e.target.value;
                    this.handleFilterChange();
                }}
                >
                  <option value="">Sin orden</option>
                  <option value="date-asc">Fecha (Próximas primero)</option>
                  <option value="date-desc">Fecha (Últimas primero)</option>
                  <option value="priority-asc">Prioridad (Crítica primero)</option>
                  <option value="priority-desc">Prioridad (Baja primero)</option>
                </select>
                <button class="clear-filter-btn" @click=${this.handleClearFilters}>
                  Limpiar Filtros
                </button>
              </div>
            </div>
            ` : ''}
        
        <table class="tasks-table ${!this.isLoading && this.filteredTasks.length > 0 ? 'show' : ''}">
          <thead>
            <tr>
              <th>Tarea</th>
              <th>Estado</th>
              <th>Fecha de Ejecución</th>
              <th>Prioridad</th>
              <th>Asignada a</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            ${this.filteredTasks.map(task => html`
              <tr>
                <td class="task-title">${this.escapeHtml(task.title)}</td>
                <td>
                  <span class="task-status ${this.escapeHtml(task.status)}">
                    ${this.escapeHtml(task.status)}
                  </span>
                </td>
                <td>${this.escapeHtml(task.deadline)}</td>
                <td>
                  <span class="priority-badge priority-${task.priority}">
                    ${this.escapeHtml(task.priority)}
                  </span>
                </td>
                <td>${this.escapeHtml(task.assignee)}</td>
                <td>
                  <button 
                    class="task-details-btn" 
                    @click=${() => this.handleDetailsClick(task)}
                  >
                    Detalles
                  </button>
                </td>
              </tr>
            `)}
          </tbody>
        </table>

        <!-- Modal -->
        <div class="task-modal ${this.isModalOpen ? 'show' : ''}" @click=${this.handleModalClickOutside}>
          <div class="task-modal-content">
            <button class="task-modal-close" @click=${this.handleCloseModal}>&times;</button>
            ${this.isEditing ? this.renderModalEditMode() : this.renderModalViewMode()}
          </div>
        </div>

        <!-- Delete Confirmation Modal -->
        <div class="delete-confirm-modal">
          <div class="delete-confirm-content">
            <h2 class="delete-confirm-title">Eliminar Tarea</h2>
            <p class="delete-confirm-text">
              Esta acción no se puede deshacer. Para confirmar, escribe <strong>"delete-task"</strong> en el campo de abajo.
            </p>
            <div class="delete-confirm-input-group">
              <label class="delete-confirm-input-label" for="delete-confirm-input">Escribe para confirmar:</label>
              <input 
                type="text" 
                id="delete-confirm-input" 
                class="delete-confirm-input" 
                placeholder="delete-task"
                @input=${this.handleDeleteInput}
              >
            </div>
            <div class="delete-confirm-actions">
              <button class="delete-cancel-btn" @click=${() => {
                const modal = this.shadowRoot.querySelector('.delete-confirm-modal');
                if (modal) modal.classList.remove('show');
            }}>Cancelar</button>
              <button 
                class="delete-confirm-btn" 
                ?disabled=${this.deleteConfirmText !== 'delete-task'}
                @click=${this.handleDeleteConfirm}
              >
                Eliminar
              </button>
            </div>
          </div>
        </div>
      </div>
    `;
    }
}

customElements.define('saviia-get-tasks', SaviiaGetTasks);
logger.info("SAVIIA Get Tasks registered");