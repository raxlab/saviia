import { hass, environment, baseUrl, token } from "../services/ha-client.js";
import { createLogger } from "../services/logger.js";

const logger = createLogger("TasksAPI");


export default class TasksAPI {
    constructor() {
        this.webhookUrl = "https://discord.com/api/webhooks/1452857904926294068/1AXRVxx3blLgOHuJFZ_EYnQNgt3eVcINFv495zjcE502v8NX3XunMXtwt9JZGh2jVlJ4" // TODO: DELETE
        this.hass = hass;
        this.environment = environment;
        this._hassHeaders = {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
        logger.info("Initialized", { environment: this.environment });
    }
    async _callServiceWithErrorHandling(domain, service, data = {}) {
        try {
            logger.debug("Calling HA service", { domain, service });
            const result = await hass.callService(domain, service, data)
            logger.debug("HA service call succeeded", { domain, service });
            return result
        } catch (error) {
            logger.error(`Error while calling service ${service} at ${domain}`, error)
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
            const url = `${baseUrl}/rest_command/discord_get_tasks?return_response`
            const data = await this._fetchWithErrorHandling(url, {
                method: 'POST',
                headers: this._hassHeaders
            })
            const messages = data.service_response.content
            logger.info("Tasks fetched", { count: Array.isArray(messages) ? messages.length : 0 });
            return messages
        } else {
            const result = await this._callServiceWithErrorHandling(
                'rest_command', 'discord_get_tasks'
            )
            logger.info("Tasks fetched via hass service");
            return result
        }
    }

    async updateTask(task, completed) {
        logger.info("Updating task", { taskId: task?.tid, completed });
        const payload = JSON.stringify({
            webhook_url: this.webhookUrl,
            task: task,
            completed: completed,
        })
        if (this.environment === "development") {
            const url = `${baseUrl}/saviia/update_task?return_response`
            const result = await this._fetchWithErrorHandling(url, {
                method: 'POST',
                headers: this._hassHeaders,
                body: payload
            })
            logger.info('Task updated at Discord', { taskId: task?.tid })
            return result
        } else {
            const result = await this._callServiceWithErrorHandling(
                'saviia', 'update_task?return_response', payload
            )
            logger.info('Task updated via hass service', { taskId: task?.tid })
            return result;
        }
    }

    async deleteTask(taskId) {
        logger.info("Deleting task", { taskId });
        const payload = JSON.stringify({
            webhook_url: this.webhookUrl,
            task_id: taskId
        })
        if (this.environment === "development") {
            const url = `${baseUrl}/saviia/delete_task?return_response`
            const result = await this._fetchWithErrorHandling(url, {
                method: 'POST',
                headers: this._hassHeaders,
                body: payload
            })
            logger.info('Task deleted at Discord', { taskId })
            return result
        } else {
            const result = await this._callServiceWithErrorHandling(
                'saviia', 'delete_task?return_response', payload
            )
            logger.info('Task deleted via hass service', { taskId })
            return result;
        }
    }
}