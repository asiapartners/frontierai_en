# Part 2: Microsoft AI Agentic Workshop

> Note: Read the workshop scenario overview [here](SCENARIO.md) before starting setup.

## Step 1: Workshop Setup
This step guides you through setting up environment variables.

## Prerequisites
- Azure Subscription
- Prior Knowledge:
    - Azure subscriptions and resources
    - GitHub Mechanics (account creation, repository cloning, etc.)
  
### 1. Verify Repository and .env File Locations

The AI application to be run in Part 2 will operate from the mcp and agentic_ai directories in the `frontieraid_en` repository cloned in the previous step.

> Part 2's Hands-on Lab uses 2 .env files.
* ./mcp/.env.sample ==> .env for MCP server
* ./agentic_ai/application/.env.sample ==> .env for Agent application

### 2. Deploy LLM Model in Microsoft Foundry

Use the Microsoft Foundry project and GPT-4.1 model deployed in [the previous step](1_basic_concept.md).
  
### 3. Set Environment Variables
  
Rename the `.env.sample` file in the `agentic_ai/applications` folder to `.env` and fill in all required fields. Here is a sample configuration:  
  
```bash  
############################################  
#  Azure OpenAI – chat model configuration #  
############################################  
# Replace with your model-deployment endpoint in Azure AI Foundry  
AZURE_OPENAI_ENDPOINT="https://YOUR-OPENAI-SERVICE-ENDPOINT.openai.azure.com"  
  
# Replace with your Foundry project's API key  
AZURE_OPENAI_API_KEY="YOUR-OPENAI-API-KEY"  
  
# Connection-string that identifies your Foundry project / workspace. Only needed if you're using Azure Agent Service
AZURE_AI_AGENT_PROJECT_CONNECTION_STRING="YOUR-OPENAI-PROJECT-CONNECTION-STRING"  
  
# Model deployment & API version  
AZURE_OPENAI_CHAT_DEPLOYMENT="gpt-4.1"  
AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME="gpt-4.1" # only needed if you're using Azure Agent Service 
AZURE_OPENAI_API_VERSION="2025-01-01-preview"  
OPENAI_MODEL_NAME="gpt-4.1-2025-04-14"  #only applicable for Autogen
  
############################################  
#     Local URLs for backend & MCP server  #  
############################################  
BACKEND_URL="http://localhost:7000"  
MCP_SERVER_URI="http://localhost:8000/mcp"  
  
############################################  
#         Agent module to be executed      #  
############################################  
AGENT_MODULE="agents.agent_framework.single_agent"
# AGENT_MODULE="agents.agent_framework.multi_agent.handoff_multi_domain_agent"
# AGENT_MODULE="agents.agent_framework.multi_agent.magentic_group"
  
############################################  
#       State store configuration          #
############################################
DATA_TENANT_ID="default"  
```
  
### 4. Deploy Embedding Model to Microsoft Foundry

1. In Microsoft Foundry, deploy a model from **Models + endpoints** within the same project.
    
    <img src="images/step3-01.png" width="720"/>

2. Select the text-embedding-ada-002 model.

    <img src="images/step3-02.png" width="500"/>

3. Select **Global Standard** for deployment type or your preferred region.

    <img src="images/step3-03.png" width="500"/>

4. From the source repository, navigate to the root folder, then go to the `mcp` folder, rename the `.env.sample` file to `.env`, and fill in all required fields. Here is a sample configuration:
  
    ```bash
    # This file is a sample configuration for the MCP backend services's knowledge retrieval APIs which uses text-embedding-ada-002 embedding model
    AZURE_OPENAI_ENDPOINT="YOUR-OPENAI-SERVICE-ENDPOINT.openai.azure.com"
    AZURE_OPENAI_API_KEY="YOUR-OPENAI-API-KEY"
    AZURE_OPENAI_API_VERSION=2025-03-01-preview
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT="text-embedding-ada-002"
    DB_PATH="data/contoso.db"
    AAD_TENANT_ID=""
    MCP_API_AUDIENCE=""
    MCP_SERVER_URI="http://localhost:8000/mcp"
    DISABLE_AUTH="true"
    ```


**Ensure your Azure resources are configured with the correct model deployment names, endpoints, and API versions.**
  
---

## Next Step: MCP Server
Once the `.env` file is configured, you can start the MCP server.

* [Hands-on Lab 1 – MCP Server](2_01_mcp_uv.md)

## Lab Sequence

### Part 1
* [Microsoft Agent Framework Basic Concept HoL](00_basic_concept.md)

### Part 2
* [Hands-on Lab 0 – Setup](2_00_setup.md)
* [Hands-on Lab 1 – MCP Server](2_01_mcp_uv.md)
* [Hands-on Lab 2 – Backend](2_02_backend_uv.md)
* [Hands-on Lab 3 – Frontend](2_03_frontend_react.md)

