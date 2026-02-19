import {
    css,
} from "https://unpkg.com/lit-element@2.4.0/lit-element.js?module";

export const generalStyle = css`

body {
    width: 100%;
    min-height: 100vh;
    margin: 0;
    background-color: #f5f5f5;
    color: #212121;
    font-size: clamp(14px, 2vw, 16px);
}
h1, h2, h3, h4, h5, h6, p {
    text-align: center;
}
fieldset legend, fieldset p {
    text-align: left;
}
h1, h2, h3, h4, h5, h6, p, i, legend, label, td, th {
    margin: 1em auto;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.filters-sort-container {
    max-width: 80vw;
    margin: 2em auto;
    padding: 1.5em;
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    
    flex-wrap: wrap;
}

.filters-group,
.sort-group {
    display: flex;;
    gap: 1em;
    align-items: center;
    flex-wrap: wrap;
}

.filters-group label,
.sort-group label {
    font-weight: 600;
    color: #212121;
}

.filters-group select,
.filters-group input,
.sort-group select {
    padding: 0.5em 0.75em;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
    background-color: #ffffff;
    cursor: pointer;
}

.filters-group select:focus,
.filters-group input:focus,
.sort-group select:focus {
    outline: none;
    border-color: #212121;
    box-shadow: 0 0 3px rgba(33, 33, 33, 0.2);
}

.clear-filter-btn {
    padding: 0.5em 1em;
    background-color: #f5f5f5;
    border: 1px solid #ddd;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.2s;
}

.clear-filter-btn:hover {
    background-color: #eeeeee;
}


@media (max-width: 768px) {
    body {
        font-size: clamp(12px, 3vw, 14px);
    }
    
    h1 {
        font-size: 2.5rem;
    }
    
    h2, h3 {
        font-size: 2rem;
    }
    
    h4, h5, h6 {
        font-size: .9rem;
    }
    
    p {
        font-size: 1rem;
    }
}

`