import { createLogger } from "../services/logger.js";

const logger = createLogger("TasksAPI");


export default class TasksAPI {
    constructor(hass = null) {
        this.hass = hass;
        this.environment = window.location.origin.includes("homeassistant")
            ? "production"
            : "development";
        if (this.environment === "development") {
            this.baseUrl = import.meta.env?.VITE_HA_URL;
            this.token = import.meta.env?.VITE_HA_TOKEN;
            this._hassHeaders = {
                'Authorization': `Bearer ${this.token}`,
                'Content-Type': 'application/json'
            }
        }
        logger.info("Initialized", { environment: this.environment });
    }
    async _callServiceWithErrorHandling(domain, service, data = {}) {
        try {
            const result = await this.hass.callApi(
                "POST",
                `services/${domain}/${service}?return_response`,
                data
            );
            return result;
        } catch (error) {
            logger.error(`Error while calling service ${service}`, error);
            throw new Error(`Home Assistant service error: ${error.message}`);
        }
    }
    async _fetchWithErrorHandling(url, options = {}) {
        try {
            logger.debug("HTTP request started", { url, method: options.method ?? "GET" });
            const response = await fetch(url, options);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            logger.debug("HTTP request succeeded", { url, status: response.status });
            return await response.json();
        } catch (error) {
            logger.error("HTTP request failed", { url, error: error.message });
            throw new Error(`Internal error: ${error.message}`);
        }
    }
    async getTasks() {
        logger.info("Fetching tasks");
        if (this.environment === "development") {
            const url = `${this.baseUrl}/saviia/get_tasks?return_response`
            const data = await this._fetchWithErrorHandling(url, {
                method: 'POST',
                headers: this._hassHeaders
            })
            const tasks = data.service_response.api_metadata.tasks
            logger.info("Tasks fetched", { count: tasks.length });
            return tasks
        } else {
            const data = await this._callServiceWithErrorHandling('saviia', 'get_tasks')
            const messages = data.service_response.content
            logger.info("Tasks fetched via hass service", messages);
            return messages
        }
    }

    async updateTask(task, completed) {
        logger.info("Updating task", { taskId: task?.tid, completed });
        const payload = JSON.stringify({ task: task, completed: completed })
        if (this.environment === "development") {
            const url = `${this.baseUrl}/saviia/update_task?return_response`
            const result = await this._fetchWithErrorHandling(url, {
                method: 'POST',
                headers: this._hassHeaders,
                body: payload
            })
            logger.info('Task updated at Discord', { taskId: task?.tid })
            return result
        } else {
            const result = await this._callServiceWithErrorHandling('saviia', 'update_task', payload);
            logger.info('Task updated via hass service', { taskId: task?.tid }, result)
            return result;
        }
    }

    async deleteTask(taskId) {
        logger.info("Deleting task", { taskId });
        const payload = JSON.stringify({ task_id: taskId })
        if (this.environment === "development") {
            const url = `${this.baseUrl}/saviia/delete_task?return_response`
            const result = await this._fetchWithErrorHandling(url, {
                method: 'POST',
                headers: this._hassHeaders,
                body: payload
            })
            logger.info('Task deleted at Discord', { taskId })
            return result
        } else {
            const result = await this._callServiceWithErrorHandling('saviia', 'delete_task', payload);
            logger.info('Task deleted via hass service', { taskId }, result)
            return result;
        }
    }

    async createTask(task, images = []) {
        logger.info("Creating task", { task });
        const payload = { task: task, images: images }
        if (this.environment === "development") {
            const url = `${this.baseUrl}/saviia/create_task?return_response`
            const result = await this._fetchWithErrorHandling(url, {
                method: 'POST',
                headers: this._hassHeaders,
                body: JSON.stringify(payload)
            })
            logger.info('Task created successfully at Discord', { task }, { images: images.length })
            return result
        } else {
            const result = await this._callServiceWithErrorHandling('saviia', 'create_task', payload);
            logger.info('Task created via hass service', { task }, result)
            return result;
        }
    }
}