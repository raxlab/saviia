import { defineConfig } from "vite";

export default defineConfig({
    build: {
        outDir: "../dist",
        emptyOutDir: true,
        rollupOptions: {
            input: "./src/saviia-panel.ts",
            output: {
                entryFileNames: "saviia-panel.js",
            },
        },
    },
});
