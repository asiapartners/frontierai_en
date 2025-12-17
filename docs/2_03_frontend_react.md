# Part 2: Microsoft AI Agentic Workshop

## Step 4: Frontend Setup with React

This step sets up and runs the React frontend for the Microsoft AI Agentic Workshop. The React frontend provides advanced streaming visualization that is ideal for Microsoft Agent Framework agents, offering real-time token-by-token streaming and internal agent process visibility.

## Prerequisites
- [Step 1: Workshop Setup](2_00_setup.md) completed
- [Step 2: MCP Setup (uv)](2_01_mcp_uv.md) completed
- [Step 3: Backend Setup (uv)](02_backend_uv.md) completed
- MCP running verification: `http://localhost:8000/mcp`
- Backend service running verification: `http://localhost:7000/chat`

### 1. Install Node.js

Running the React Frontend requires Node.js 16 or higher and npm.

> **Action Items:**
> Open a new terminal window, separate from the ones running the MCP server and backend.
> ![new terminal](media/01_mcp_new_terminal.png)
> Verify that Node.js and npm are installed:
> ```bash
> node --version  # Should be v16 or higher
> npm --version   # Should be v8 or higher
> ```
> 
> If not installed, choose one of the following installation methods:
> - **Windows/macOS/Linux:** Download and install the LTS version from [https://nodejs.org/](https://nodejs.org/).
> - **Windows (alternative):** Use the command `winget install OpenJS.NodeJS.LTS`.
> - **macOS (alternative):** Use the command `brew install node`.

### 2. Frontend Configuration (optional)

The React frontend connects to `http://localhost:7000` by default.

> **Action Items (Optional):**
> To customize the Backend URL, create a `.env` file in the `react-frontend` directory:
> ```bash
> # react-frontend/.env
> REACT_APP_BACKEND_URL=http://localhost:7000
> ```

### 3. Install Dependencies and Start React Frontend

> **Action Items:**
> Navigate to the React frontend directory from `agentic_ai/applications`:
> ```bash
> cd react-frontend
> ```
> 
> Install Dependencies (first run or after package.json changes):
> ```bash
> npm install
> ```
> 
> Start the React development server:
> ```bash
> npm start
> ```
> 
> The React app will automatically open at `http://localhost:3000`. If it doesn't open automatically, navigate to `http://localhost:3000` in your browser.

## Success Criteria
- React frontend should be running at `http://localhost:3000`.
- Frontend should successfully connect to Backend at `http://localhost:7000`.
- You should be able to interact with the AI agent through the Chat interface.
- Real-time streaming and agent process visibility should be working.

    <img src="media/03_frontend_react_chat.png" />

> Note: Try interacting with the agent using the following prompt:
> ```
> What can you help me with?
> ```

- Chat with the agent and observe real-time token streaming and internal agent behavior (e.g., tool calls, planning steps).

    <img src="media/03_frontend_magentic_steps.png" />

> Note: Use the following prompt to check internal agent behavior:
> ```
> Please retrieve the most recent invoice for customer 101, including line items and total charges. Additionally, compare it with previous invoices to identify why the latest invoice is higher and note any new charges, fee changes, expired discounts, upgrades, or other relevant issues. Cite relevant tool results and data references in your response.
> ```
  
## Troubleshooting
- **Is port 3000 already in use?** The React app will ask if you want to use a different port. Enter `Y` to accept.
- **npm install failing?** Try clearing the npm cache and retry: `npm cache clean --force`
- **WebSocket connection errors?** Verify that the backend is running on port 7000 and that the firewall is not blocking the connection.

**Congratulations**: If you have successfully completed all steps, the setup is complete and your agents should be running! For more details, see [How It Works →](2_04_how_it_works.md).

## Next Step
If you have successfully finished Frontend App lab, you can go to optional 

* [Human-in-the-Loop Patterns in Microsoft Agent Framework](https://github.com/asiapartners/frontierai_en/blob/main/docs/3_%5Boptional%5Dhuman_in_the_loop.md)

## Lab

### Part 1
* [Microsoft Agent Framework Basic Concept HoL](00_basic_concept.md)

### Part 2
* [Hands-on Lab 0 – Setup](2_00_setup.md)
* [Hands-on Lab 1 – MCP Server](2_01_mcp_uv.md)
* [Hands-on Lab 2 – Backend](2_02_backend_uv.md)
* [Hands-on Lab 3 – Frontend](2_03_frontend_react.md)

