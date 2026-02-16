import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";
import "./index.css";

const rootElement = document.getElementById("root");

if (rootElement) {
  const root = createRoot(rootElement);

  root.render(
    <StrictMode>
      <App />
    </StrictMode>
  );
}

export function mountApp(container, hass) {
  const root = createRoot(container);

  root.render(
    <StrictMode>
      <App hass={hass} />
    </StrictMode>
  );
}
