import {
    css,
} from "https://unpkg.com/lit-element@2.4.0/lit-element.js?module";


export const alertStyle = css`
.custom-alert {
    padding: 1em 1.5em;
    border-radius: 0.5em;
    font-size: 1.1em;
    width: 90%;
    max-width: 400px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    opacity: 1;
    transition: opacity 1s ease-in-out;
    animation: slideDown 0.5s ease forwards;
    z-index: 2000;
    position: fixed;
    top: 2em;
    left: 50%;
    transform: translateX(-50%);
    margin: 0;
    text-align: center;
}

.custom-alert-info {
    background: #03a9f4;
    color: #ffffff;
}

.custom-alert-success {
    background: #43a048d1;
    color: #ffffff;
}

.custom-alert-danger {
    background: #e53835e7;
    color: #ffffff;
}

.custom-alert.fade-out {
    opacity: 0;
    animation: slideOut 0.5s ease forwards;
}

@keyframes slideDown {
    0% {
        transform: translateX(-50%) translateY(-20px);
        opacity: 0;
    }
    100% {
        transform: translateX(-50%) translateY(0);
        opacity: 1;
    }
}

@keyframes slideOut {
    0% {
        transform: translateX(-50%) translateY(0);
        opacity: 1;
    }
    100% {
        transform: translateX(-50%) translateY(-20px);
        opacity: 0;
    }
}
`