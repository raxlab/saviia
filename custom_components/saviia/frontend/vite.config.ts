import { defineConfig } from "vite";

export default defineConfig({
    build: {
        outDir: "custom_components/saviia/frontend",
        emptyOutDir: true,
        rollupOptions: {
            input: "./src/saviia-panel.ts",
            output: {
                entryFileNames: "saviia-panel.js",
            },
        },
    },
});
