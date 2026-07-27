import { Composio } from "@composio/core";
import { VercelProvider } from "@composio/vercel";
import * as fs from "fs";
import { spawn } from "child_process";

async function main() {
    console.log("Initializing Composio MCP Session...");
    
    // Ensure API Key is available
    const apiKey = process.env.COMPOSIO_API_KEY || "ak_bX8LiMzAhd6al7KJ5wdJ";
    const composio = new Composio({ apiKey, provider: new VercelProvider() });
    
    // Create a dynamic Tool Router session (this replaces the old static Server ID)
    const session = await composio.create("user_gf9by");
    
    if (!session.mcp || !session.mcp.url) {
        throw new Error("Failed to generate MCP URL from Composio!");
    }
    
    console.log(`Successfully generated MCP URL: ${session.mcp.url}`);
    
    // Construct the mcp_config.json dynamically
    const mcpConfig = {
        mcpServers: {
            composio: {
                serverUrl: session.mcp.url,
                headers: session.mcp.headers || {
                    "x-api-key": apiKey
                }
            }
        }
    };
    
    // Write it to the config file so Antigravity can use it
    fs.writeFileSync(".agents/mcp_config.json", JSON.stringify(mcpConfig, null, 2));
    console.log("Updated .agents/mcp_config.json securely.");
    
    console.log("Starting Antigravity CLI...");
    console.log("\n=======================================================");
    console.log("When the UI loads, paste this exact prompt and hit Enter:");
    console.log("Begin the research pipeline on the apps in data/apps_list.json");
    console.log("=======================================================\n");
    
    // Launch the AGY CLI, inheriting stdio so the TUI works properly!
    const agy = spawn("agy", ["run", ".agents/agents/lead-researcher.md"], {
        stdio: "inherit"
    });
    
    agy.on("close", (code) => {
        console.log(`Pipeline finished with code ${code}`);
    });
}

main().catch(console.error);
