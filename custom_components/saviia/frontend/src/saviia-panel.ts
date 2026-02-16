import { LitElement, html } from "lit";
import { CreateTask } from "./components/tasks/create-task/create-task";


export class SaviiaPanel extends LitElement {
    render() {
        return html`
    <create-task></create-task>
    `;
    }
}

customElements.define("saviia-panel", SaviiaPanel);
