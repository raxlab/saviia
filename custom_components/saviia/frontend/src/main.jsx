import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";
import "./index.css";

export function mountApp(container, hass) {
  const root = createRoot(container);
  root.render(
    <StrictMode>
      <App hass={hass} />
    </StrictMode>
  );
}

export function updateApp(hass) {
  if (root) {
    root.render(
      <StrictMode>
        <App hass={hass} />
      </StrictMode>
    )
  }
}