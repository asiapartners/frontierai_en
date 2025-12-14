# Part 2: Microsoft AI Agentic Workshop

## Step 3: Application Backend Server

This step configures and runs the backend service for the Microsoft AI Agentic Workshop using uv. The backend fully supports Microsoft's Agent Framework with advanced multi-agent capabilities.

## Prerequisites
- [Step 1: Workshop Setup](2_00_setup.md) completed
- [Step 2: MCP Setup (uv)](2_01_mcp_uv.md) completed
- MCP running verification: `http://localhost:8000/mcp`
- uv installation completed

## Microsoft Agent Framework Options

**Single Agent (`agents.agent_framework.single_agent`):**
- One agent handles all tasks. (Suitable for simple scenarios: FAQ, basic support, etc.)
- Basic ChatAgent with MCP tools
- Token-by-token streaming via WebSocket
- Tool call visibility in React UI
- Session state persistence across requests

**Magentic Multi-Agent (`agents.agent_framework.multi_agent.magentic_group`):**
- Multiple agents solve problems through collaborative dialogue.
- Intelligent orchestrator coordinates specialist agents (CRM/Billing, Product/Promotions, Security)
- Real-time streaming of orchestrator planning and agent responses
- Custom progress ledger for human-in-the-loop support
- Checkpointing for resumable workflows
- React UI shows full internal process: task ledger, instructions, agent tool calls

**Handoff Multi-Agent (`agents.agent_framework.multi_agent.handoff_multi_domain_agent`):**
- One agent handles all tasks. (Suitable for simple scenarios: FAQ, basic support, etc.)
- Direct agent-to-user communication with intelligent domain routing
- Configurable context transfer between specialists (preserves customer info, history)
- Smart intent classification for seamless handoffs
- Cost-efficient (33% fewer LLM calls vs orchestrator patterns)

### 1. Agent Framework Setup

> **Action Items:**
> In the `.env` file in the `agentic_ai/applications` folder, uncomment one of the following lines:
> ```bash
> # In your .env file in agentic_ai/applications folder, uncomment one of following for agent framework:
> AGENT_MODULE="agents.agent_framework.single_agent"
> # OR
> AGENT_MODULE="agents.agent_framework.multi_agent.magentic_group"
> # OR
> AGENT_MODULE="agents.agent_framework.multi_agent.handoff_multi_domain_agent"
> ```
> 
> Add additional environment variables to the bottom of your existing `.env` file:
> 
> **For Magentic Orchestration Settings (magentic_group):**
> ```bash
> MAGENTIC_LOG_WORKFLOW_EVENTS=true
> MAGENTIC_ENABLE_PLAN_REVIEW=false  # Set to true for human-in-the-loop plan approval
> MAGENTIC_MAX_ROUNDS=10
> ```
> 
> **For Handoff Agent Context Transfer (handoff_multi_domain_agent):**
> ```bash
> HANDOFF_CONTEXT_TRANSFER_TURNS=-1  # -1=all history, 0=none, N=last N turns
> ```
  
📚 **[Check detailed pattern guide and settings →](../agentic_ai/agents/agent_framework/README.md)**

### 2. Run Backend Service

> **Action Items:**
> Open a new terminal window, separate from the one running the MCP server.
> ![new terminal](media/01_mcp_new_terminal.png)
> Navigate to the applications directory and start the backend:
> ```bash
> cd agentic_ai/applications
> uv run python backend.py
> ```

### 3. Choose Frontend Experience

## 📊 Frontend Comparison

| Feature | React Frontend | Streamlit Frontend |
|---------|---------------|-------------------|
| **Real-time streaming** | ✅ Token-by-token | ❌ Full response only |
| **Internal process visibility** | ✅ Orchestrator, agents, tools | ❌ Final answer only |
| **Tool call tracking** | ✅ Per-turn history | ❌ Not shown |
| **Multi-agent visualization** | ✅ Agent timeline & planning | ❌ Not shown |
| **Best for Agent Framework** | ✅ **Recommended** | ⚠️ Basic support |
| **Setup complexity** | Medium (npm install) | Low (no additional setup) |
| **Best use case** | Development, demos, debugging | Quick testing, simple chat |

**Recommendation:**
- Use React: See the full multi-agent orchestration of Agent Framework agents.
- Use Streamlit: Conduct quick testing or simple demos of all agent types.
- This lab uses the React frontend.

## Success Criteria
- Backend service should be running at `http://localhost:7000`.

- Agent Framework should be properly configured.

- Backend should be able to communicate with the MCP server.
  - Run the sample PowerShell command below to validate the Backend server:
    ```powershell
    # Define the URL
    $uri = "http://localhost:7000/chat"
  
    # Define headers
    $headers = @{
        Accept = "application/json"
        "Content-Type" = "application/json"
    }
    
    # Define the JSON body
    $body = @{
        session_id = "123"
        prompt     = "What can you help me with?"
    } | ConvertTo-Json
    
    # Send the POST request
    $response = Invoke-WebRequest -Uri $uri -Method POST -Headers $headers -Body $body
    
    # Output the response
    $response.Content
    ```
    <img src="media/02_backend_chat_response.png" />
 
  - A sample curl command to validate things are online:
    ```bash
    `curl -X 'POST' 'http://localhost:7000/chat'  -H 'accept: application/json'  -H 'Content-Type: application/json'  -d '{"session_id": "123", "prompt": "What can you help me with?"}'`
    ```

- Backend should be able to communicate with the MCP server.
  - Sample curl command to check online status: `curl -X 'POST' 'http://localhost:7000/chat'  -H 'accept: application/json'  -H 'Content-Type: application/json'  -d '{"session_id": "123", "prompt": "What can you help me with?"}'`

    **Note:** The local server does not return AI responses. If checking in a browser, the error below is expected behavior.

    <img src="media/02_backend_localhost_err.png" />

- Should be ready to connect with the frontend.

## Next Step: Frontend Service

* [Hands-on Lab 3 – Frontend](2_03_frontend_react.md)

## Lab Sequence

### Part 1
* [Microsoft Agent Framework Basic Concept HoL](00_basic_concept.md)

### Part 2
* [Hands-on Lab 0 – Setup](2_00_setup.md)
* [Hands-on Lab 1 – MCP Server](2_01_mcp_uv.md)
* [Hands-on Lab 2 – Backend](2_02_backend_uv.md)
* [Hands-on Lab 3 – Frontend](2_03_frontend_react.md)


**📌 Important:** Agent Framework works best with the **React frontend** when visualizing internal agent processes, orchestrator plans, and tool calls in real-time.

