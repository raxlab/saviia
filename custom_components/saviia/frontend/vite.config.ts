import { defineConfig } from "vite";

export default defineConfig({
    build: {
        outDir: "../dist",
        emptyOutDir: true,
        rollupOptions: {
            output: {
                entryFileNames: "saviia-panel.js",
            },
        },
    },
});
