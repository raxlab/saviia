import { css } from 'lit';

export const tableStyle = css`
.tasks-table {
    width: 90%;
    max-width: 1200px;
    margin: 2em auto;
    border-collapse: collapse;
    background-color: #ffffff;
    border-radius: 0.5em;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    max-height: 70vh;
    overflow-y: auto;
}

.tasks-table thead {
    color: gray;
}

.tasks-table th {
    padding: 1em;
    text-align: left;
    font-size: 1em;
    color: black;
}

.tasks-table td {
    padding: 1em;
    border-bottom: 1px solid #dcdada;
    color: #212121;
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
    background-color: var(--color-accent, #007bff);
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
    font-weight: bold;
    transition: background-color 0.3s ease;
}

.header-action-btn:hover {
    background-color: var(--color-accent-dark, #0056b3);
    opacity: 0.9;
}

.header-action-btn:active {
    transform: scale(0.98);
}

@media (max-width: 768px) {
    .tasks-table {
        width: 95%;
        font-size: 0.9em;
    }

    .tasks-table th,
    .tasks-table td {
        padding: 0.75em 0.5em;
    }

    .task-description {
        max-width: 150px;
    }
}
`
