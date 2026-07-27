# Composio SaaS Research Framework

This is a generalized framework directory designed to run a multi-agent research pipeline using the Antigravity CLI (`agy`) and Composio. It evaluates a batch of SaaS applications and generates verified JSON reports on their viability as AI agent toolkits.

## 🛠️ Setup Instructions

### 1. Duplicate the Framework
Do **not** run the pipeline directly in this generalized template directory. Copy this entire folder to a new location for your specific run:
```bash
cp -r composio-research /path/to/new/run-directory
cd /path/to/new/run-directory
```

### 2. Prepare Your Data
Update `data/apps_list.json` with the list of applications you want the agents to research. Ensure it contains valid JSON.

### 3. API Key
Open the `.env` file (create it if missing) and add your Composio API key:
```env
COMPOSIO_API_KEY=your_api_key_here
```

## 🚀 How to Run the Pipeline

Because Composio manages tool integrations dynamically, you don't need to manually configure the MCP server! We've provided a script that dynamically requests a secure session from Composio, configures the agent, and launches the pipeline for you.

1. Install dependencies (only needed once):
   ```bash
   npm install @composio/core @composio/vercel tsx
   ```

2. Run the launch script:
   ```bash
   npx tsx start_pipeline.ts
   ```

3. The Antigravity Terminal User Interface (TUI) will launch automatically. When prompted for input, paste the following exact command to trigger the orchestration:
   ```text
   Begin the research pipeline on the apps in data/apps_list.json
   ```

4. Press **Enter**. 
   - The Lead Researcher will initialize the `data/state/task_queue.json`.
   - It will begin spawning `research-worker` subagents in batches of 5.
   - As workers finish, the orchestrator will pass batches to the `verifier` and eventually to the `report-builder`.
   - You can view all tool executions live in the **Composio Dashboard** (under Execution Logs)!

## 📁 Directory Structure
- `start_pipeline.ts`: Unified launch script that configures MCP and starts the AGY CLI.
- `.agents/`: Contains agent definitions (`lead-researcher.md`, `research-worker.md`, etc.), skill rules, and the auto-generated `mcp_config.json`.
- `data/`: Contains `apps_list.json` (input) and `schema.json` (output contract).
- `data/state/`: Tracks in-progress research (`task_queue.json`).
- `data/raw/`: Raw output from research-workers.
- `data/verified/`: Final output after verification.
