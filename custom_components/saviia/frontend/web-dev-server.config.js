import * as fs from 'fs';
import * as path from 'path';

// Load env variables
function loadEnv() {
    const envPath = path.resolve('.env.local');
    const env = {};

    if (fs.existsSync(envPath)) {
        const content = fs.readFileSync(envPath, 'utf-8');
        content.split('\n').forEach(line => {
            const [key, value] = line.split('=');
            if (key && value) {
                env[key.trim()] = value.trim().replace(/^["']|["']$/g, '');
            }
        });
    }

    return env;
}

const env = loadEnv();

const envPlugin = {
    name: 'env-plugin',
    transform(context) {
        if (context.response.is('js') || context.request.url.endsWith('.js') || context.request.url.endsWith('.ts')) {
            let code = context.body;
            if (code && typeof code === 'string') {
                let envObj = '{';
                Object.entries(env).forEach(([key, value]) => {
                    envObj += `${key}: "${value}", `;
                });
                envObj += '}';

                code = `Object.assign(import.meta, {env: ${envObj}});\n${code}`;
            }
            return { body: code };
        }
    }
};

export default {
    open: true,
    watch: true,
    appIndex: 'index.html',
    nodeResolve: {
        exportConditions: ['development'],
    },
    plugins: [envPlugin],
};