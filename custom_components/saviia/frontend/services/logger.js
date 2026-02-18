const LOG_LEVELS = {
    debug: 10,
    info: 20,
    warn: 30,
    error: 40,
    silent: 100,
};

const DEFAULT_LEVEL = import.meta.env?.VITE_LOG_LEVEL
    ? String(import.meta.env.VITE_LOG_LEVEL).toLowerCase()
    : (import.meta.env?.DEV ? "debug" : "info");

function resolveLevel(level) {
    return LOG_LEVELS[level] ?? LOG_LEVELS.info;
}

function canLog(currentLevel, messageLevel) {
    return resolveLevel(messageLevel) >= resolveLevel(currentLevel);
}

function formatScope(scope, args) {
    return scope ? [`[${scope}]`, ...args] : args;
}

export function createLogger(scope, level = DEFAULT_LEVEL) {
    return {
        debug: (...args) => {
            if (!canLog(level, "debug")) return;
            console.debug(...formatScope(scope, args));
        },
        info: (...args) => {
            if (!canLog(level, "info")) return;
            console.info(...formatScope(scope, args));
        },
        warn: (...args) => {
            if (!canLog(level, "warn")) return;
            console.warn(...formatScope(scope, args));
        },
        error: (...args) => {
            if (!canLog(level, "error")) return;
            console.error(...formatScope(scope, args));
        },
    };
}
