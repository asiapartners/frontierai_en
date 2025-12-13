# Part 2: Microsoft AI Agentic Workshop

> Note: Read the workshop scenario overview [here](../SCENARIO.md) before starting setup.

## Step 2: MCP Server
This step sets up the MCP (Model Control Protocol) for applications. To do this, we will install the required Python dependencies and run the MCP server.

## Prerequisites
- [Step 1: Workshop Setup](2_00_setup.md) completed

### 1. Install uv

- ⚡Quick setup with `uv`

- [**uv**](https://github.com/astral-sh/uv) is an faster Python package installer written in Rust. It's faster than `pip` and automatically manages virtual environments.

    > **Action Items:**
    > Install `uv` by running the following command in your terminal:
    > Windows (PowerShell):
    ```bash
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
    > macOS/Linux:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
 
2. Install dependencies with uv:

    > Note: uv automatically creates .venv and installs dependencies from pyproject.toml.
    > **Action Items**:
    > Navigate to the `agentic_ai/applications` folder, then run the following command to install dependencies:
    ```bash
    # Navigate to the agentic_ai/applications directory
    cd agentic_ai/applications

    # Create Virtual Environment and install all dependencies at once
    uv sync
    ```

3. Create MCP Service

> **Action Items:**
> Follow the steps below to code the `mcp_service.py` file to create the backend service. This will help you understand how to set up and run the MCP server.

Note: If you're currently in the `agentic_ai/applications` folder, first return to the root folder:

```bash
cd ../..
```

3a: Import FastMCP

Add the following import statement at the top of the `mcp_service.py` file:

    > Note: fastmcp is an MCP implementation of the Microsoft Agent Framework. It provides tools and decorators to easily set up and run an MCP server.
    > **Action Items:**
    > Note: If fastmcp is not installed, install it using the `python -m pip install fastmcp` command.
    
```python
from fastmcp import FastMCP
```

3b: Declare MCP

Declare the MCP instance in the `mcp_service.py` file as follows. Find the keyword "insert FastMCP initialization code here" and replace it with the following code:

```python
mcp = FastMCP(
    name="Contoso Customer API as Tools",
    instructions=(
        "All customer, billing and knowledge data is accessible ONLY via the declared "
        "tools below.  Return values follow the pydanticschemas.  Always call the most "
        "specific tool that answers the user's question."
    ),
    auth=auth,  
)
```

3c: Write MCP Tools

Add the following MCP tools to the `mcp_service.py` file. These tools define endpoints for interacting with customer data. Find the keyword "insert tool endpoint code here 1" and replace it with the following code:

**Tool 1: List All Customers**
```python
@mcp.tool(description="List all customers with basic info")
async def get_all_customers() -> List[CustomerSummary]:  
    data = await get_all_customers_async()
    return [CustomerSummary(**r) for r in data]
```

Find the keyword "insert tool endpoint code here 2" and replace it with the following code:

**Tool 2: Get Subscription Detail**

```python
@mcp.tool(  
    description=(  
        "Detailed subscription view → invoices (with payments) + service incidents."  
    )  
)  
async def get_subscription_detail(  
    subscription_id: Annotated[int, "Subscription identifier value"],  
) -> SubscriptionDetail:  
    data = await get_subscription_detail_async(subscription_id)

    # Convert nested data to Pydantic models
    invoices = []
    for inv_data in data['invoices']:
        payments = [Payment(**p) for p in inv_data['payments']]
        invoices.append(Invoice(**{**inv_data, 'payments': payments}))
    
    service_incidents = [ServiceIncident(**si) for si in data['service_incidents']]
    
    return SubscriptionDetail(**{**data, 'invoices': invoices, 'service_incidents': service_incidents})
```

3d: Run MCP Server

Finally, find the keyword "insert Run MCP Server code here" at the bottom of the `mcp_service.py` file and add the following code to start the MCP server:

```python
if __name__ == "__main__":  
    asyncio.run(mcp.run_http_async(host="0.0.0.0", port=8000))  
```

4. Start MCP Server

    > **Action Items:**
    > Note: If you're currently in the `agentic_ai/applications` folder, first return to the root folder:
    ```bash
    cd ../..
    ```
    > Navigate to the `mcp` folder and start the MCP server:
    ```bash
    cd mcp
    uv run python mcp_service.py
    ```
    > Note: Keep the MCP server running in this terminal window. Open a new terminal window to proceed to the next step.
    
    <img src="media/01_mcp_fastmcp.jpg" />

## Success Criteria

- The MCP server is running and ready to receive requests.
- Sample PowerShell command to check MCP server status:  
    ```powershell
    Invoke-WebRequest -Uri "http://localhost:8000/mcp" -Method POST -Headers @{Accept="application/json, text/event-stream";"Content-Type"="application/json"} -Body               '{"jsonrpc":"2.0","id":"init-1","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"curl","version":"8"}}}'
    ```

    <img src="media/01_mcp_local_ok.jpg" />
    
    **Note:** This is an MCP server endpoint and cannot be accessed directly through a browser or unsupported transport methods like SSE, so use streamable HTTP transport. The error below is expected behavior in a browser.
  
    <img src="media/01_mcp_localhost_err.png" />

 - Sample curl command to verify the MCP server is online:
    ```bash
    curl -sS -i -X POST "http://localhost:8000/mcp" -H "Accept: application/json, text/event-stream" -H 'Content-Type: application/json'  --data '{"jsonrpc":"2.0","id":"init-            1","method":"initialize", "params":{"protocolVersion":"2024-11-05","capabilities":{}, "clientInfo":{"name":"curl","version":"8"}}}'`
    ```

## Next Step: Backend Server

* [Hands-on Lab 2 – Backend](2_02_backend_uv.md)

## Lab Sequence

### Part 1
* [Microsoft Agent Framework Basic Concept HoL](00_basic_concept.md)

### Part 2
* [Hands-on Lab 0 – Setup](2_00_setup.md)
* [Hands-on Lab 1 – MCP Server](2_01_mcp_uv.md)
* [Hands-on Lab 2 – Backend](2_02_backend_uv.md)
* [Hands-on Lab 3 – Frontend](2_03_frontend_react.md)

