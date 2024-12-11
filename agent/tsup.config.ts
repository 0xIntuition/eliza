import { defineConfig } from "tsup";

export default defineConfig({
    entry: ["src/index.ts"],
    outDir: "dist",
    sourcemap: true,
    clean: true,
    format: ["esm"],
    external: [
        // Node.js built-ins
        "fs", "path", "url", "better-sqlite3",
        // Workspace packages
        "@ai16z/adapter-postgres", "@ai16z/adapter-sqlite",
        "@ai16z/client-auto", "@ai16z/client-direct",
        "@ai16z/client-discord", "@ai16z/client-telegram",
        "@ai16z/client-twitter", "@ai16z/client-farcaster",
        "@ai16z/plugin-0g", "@ai16z/plugin-goat",
        "@ai16z/plugin-bootstrap", "@ai16z/plugin-coinbase",
        "@ai16z/plugin-conflux", "@ai16z/plugin-image-generation",
        "@ai16z/plugin-evm", "@ai16z/plugin-node",
        "@ai16z/plugin-solana", "@ai16z/plugin-tee",
        "@ai16z/plugin-aptos", "@ai16z/plugin-flow"
    ]
});
