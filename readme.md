# Partner Frontier AI Workshop

## Microsoft Agent Framework

<img src="docs/images/maf.png" width="600"/>

Microsoft Agent Framework is an agent development framework provided by Azure AI Foundry that supports easy creation of intelligent agents using various AI models and services.
This framework has the following characteristics:

* Flexible Architecture: Integrated with various AI models and services (Azure OpenAI, Cognitive Services, etc.) to support conversational, automation, and multimodal scenarios.
* Enterprise-grade Security and Governance: Provides authentication, permission management, and data protection features by default to ensure safe AI agent operations.
* Scalability and Developer-friendliness: Enables partners and developers to add custom features and implement fast and efficient agent workflows in conjunction with Azure AI Foundry.

## Hands-on Lab Overview

This hands-on course is part of the Partner Frontier AI campaign, a technical enablement & engagement program between Microsoft ASEAN+KR and its partners. In this course, we will cover both theory and hands-on-lab about Microsoft Agent Framework.

* In Part 1, you will understand the basic concepts of the Microsoft Agent Framework through iPython code samples using Jupyter Notebook.
* In Part 2, you will connect Microsoft Foundry with MCP server using a sample application, run Backend/Frontend apps, and practice various multi-agent orchestration patterns.

## Prerequisites (Required Tools)

* Azure Subscription: You will be deploying resources in portal.azure.com such as Microsoft Foundry and Bing Grouding. Please verify that you have the necessary permissions.
* Visual Studio Code installation: https://code.visualstudio.com/
* Python 3.13 version installation (*On some OS, Microsoft Agent Framework may not install with version 3.14.)
* Please install [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows?view=azure-cli-latest&pivots=winget) (If installed from the VS Code terminal, please restart VS Code.)

    ```
    winget install --exact --id Microsoft.AzureCLI
    ```

* Please install the following module in the Terminal.

    ```
    pip install agent-framework --pre
    ```

* Opening Terminal and Cloning Repository

>  Open a new terminal window in VS Code:

Run the following command in the terminal to clone the repository:

```bash 
git clone https://github.com/asiapartners/frontierai_en.git
```

## Azure Resources and Environment Used

* Azure OpenAI
* Bing Grounding

## .env Files

This hands-on lab uses 3 .env files. Each .env file is used for the following purposes:

### Part 1's Microsoft Agent Framework Basic Concept HoL uses 1 .env file. 
* ./1_basic_agent/.env.sample ==> .env for 1_basic-concept-with-msaf.ipynb

### Part 2's Hands-on Lab uses 2 .env files.
* ./mcp/.env.sample ==> .env for MCP server
* ./agentic_ai/application/.env.sample ==> .env for Agent application

## Lab

### Part 1
* [Microsoft Agent Framework Basic Concept HoL](docs/1_basic_concept.md)

### Part 2
* [Hands-on Lab 0 – Setup](docs/2_00_setup.md)
* [Hands-on Lab 1 – MCP Server](docs/2_01_mcp_uv.md)
* [Hands-on Lab 2 – Backend](docs/2_02_backend_uv.md)
* [Hands-on Lab 3 – Frontend](docs/2_03_frontend_react.md)

## Referenced and Cited Repositories

* The basic-concept-with-msaf.ipynb code in Part 1 was sourced from [Agent Innovator Lab](https://github.com/Azure/agent-innovator-lab). The Agent Innovator Lab repository is operated by Microsoft's AI GBB team and provides hands-on learning materials for developing AI agents based on Microsoft Azure. This repository supports developers in building and improving agents in real-world environments through various modules including RAG implementation, agent design patterns, and evaluation and optimization techniques.

* Part 2's [Microsoft AI Agentic Workshop](https://github.com/aseangps/OpenAIWorkshop) is a Microsoft-provided repository that offers workshop materials and code for building OpenAI-based intelligent solutions. Through this repository, developers can practice various patterns from single agents to multi-agent architectures using the Microsoft Agent Framework and Azure OpenAI services.


