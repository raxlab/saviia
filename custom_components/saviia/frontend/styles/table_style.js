import {
    css,
} from "https://unpkg.com/lit-element@2.4.0/lit-element.js?module";

export const tableStyle = css`
.table-container {
    width: 90%;
    max-width: 1200px;
    margin: 2em auto;
    overflow-x: auto;
    overflow-y: auto;
    max-height: 70vh;
    border-radius: 0.5em;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    -webkit-overflow-scrolling: touch;
}

.tasks-table {
    width: 100%;
    min-width: 800px;
    border-collapse: collapse;
    background-color: #ffffff;
}

.tasks-table thead {
    color: #009ac7;
    background-color: #03a8f44e;
}

.tasks-table th {
    color: #009ac7;
    padding: 1em;
    text-align: left;
    font-size: 1em;
    font-weight: 500;
    color: black;
}

.tasks-table td {
    padding: 1em;
    border-bottom: 1px solid #dcdada;
    color: #212121;
    text-align: left;
}

.tasks-table tbody tr {
    transition: background-color 0.2s ease;
}

.tasks-table tbody tr:hover {
    background-color: rgba(3, 169, 244, 0.05);
}

.tasks-table tbody tr:last-child td {
    border-bottom: none;
}

.task-title {
    font-weight: 500;
    color: #d1d1d1;
}

.task-status.Completada {
    background-color: rgba(98, 255, 6, 0.238);
    color: rgb(4, 151, 4);
}

.task-status.Pendiente {
    background-color: rgba(255, 0, 0, 0.124);
    color: rgb(229, 1, 1);
}

.task-status {
    padding: .5rem;
    border-radius: .5rem;
}

.task-description {
    max-width: 300px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: 0.9em;
    color: #757575;
}

.priority-badge {
    display: inline-block;
    padding: 0.3em 0.6em;
    border-radius: 0.3em;
    font-size: 0.85em;
    color: #ffffff;
}

.priority-1 {
    color: red;
    background-color: rgb(255, 220, 220);
}

.priority-2 {
    color: orange;
    background-color: rgb(250, 226, 182);
}

.priority-3 {
    color: rgb(205, 205, 0);
    background-color: rgb(251, 255, 182);
}

.priority-4 {
    color: rgb(6, 187, 6);
    background-color: rgb(216, 253, 216);
}
.show {
    opacity: 1
}

.loading-spinner {
    text-align: center;
    padding: 2em;
    font-size: 1.1em;
    color: #d1d1d1;
}

.header-actions {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin: 20px 0;
}

.header-action-btn {
    padding: 10px 20px;
    background-color: var(--color-accent, #03a9f4);
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
    font-weight: bold;
    transition: background-color 0.3s ease;
}

.header-action-btn:hover {
    background-color: var(--color-accent-dark, #03a9f4);
    opacity: 0.9;
}

.header-action-btn:active {
    transform: scale(0.98);
}

.header {
    max-width: 90%;
    margin: 1.4rem auto 0.4rem;
}

.meta {
    color: #64727c;
    font-size: 0.9rem;
    text-align: center;
    margin-top: 0.25rem;
}

.status-cell {
    display: inline-flex;
    align-items: center;
    gap: 0.55rem;
}

.status-dot {
    width: 0.7rem;
    height: 0.7rem;
    border-radius: 50%;
    border: 1px solid transparent;
    flex-shrink: 0;
}

.status-dot.failed {
    background: #d64747;
    border-color: #b72d2d;
    box-shadow: 0 0 0 3px rgba(214, 71, 71, 0.16);
}

.status-dot.ok {
    background: #25a35a;
    border-color: #128344;
    box-shadow: 0 0 0 3px rgba(37, 163, 90, 0.16);
}

.status-text {
    font-weight: 600;
}

.status-text.failed {
    color: #a12626;
}

.status-text.ok {
    color: #0f7940;
}

.sensor-name {
    font-weight: 600;
}

.empty {
    max-width: 90%;
    margin: 2rem auto;
    padding: 1rem;
    border-radius: 0.6rem;
    border: 1px solid #dbe3ea;
    background: #f8fafc;
    text-align: center;
    color: #4e5c67;
}

.help-text {
    color: #4e5c67;
    font-size: 0.9rem;
    text-align: center;
    margin: 0.5rem auto 1.2rem;
    max-width: 90%;
}

@media (max-width: 768px) {
    .table-container {
        width: 95%;
        max-width: 95vw;
        margin: 1em auto;
    }
    
    .tasks-table {
        min-width: 700px;
        font-size: 0.85em;
    }

    .tasks-table th,
    .tasks-table td {
        padding: 0.6em 0.4em;
        font-size: 0.9em;
    }

    .task-description {
        max-width: 120px;
    }
    
    .task-details-btn {
        padding: 0.4em 0.8em;
        font-size: 0.85em;
    }
}
`
