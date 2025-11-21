from __future__ import annotations  
  
import asyncio  
import os  
import time  
from dataclasses import dataclass, field  
from typing import Any, Optional  
  
from fastmcp import FastMCP  
from fastmcp.server import Context  
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware  
from fastmcp.server.middleware.logging import LoggingMiddleware  
from fastmcp.server.middleware.timing import TimingMiddleware  
  
# --- Import async tools from common module ---  
from contoso_tools import (  
    get_invoice_payments_async, pay_invoice_async, get_billing_summary_async,  
    unlock_account_async, get_security_logs_async,  
    get_promotions_async, get_eligible_promotions_async,   
    get_products_async, get_product_detail_async,
    get_all_customers_async, get_customer_detail_async, get_customer_orders_async,
    get_subscription_detail_async, update_subscription_async, get_data_usage_async,
    get_support_tickets_async, create_support_ticket_async,
    search_knowledge_base_async
)

# ========================================================================
# AUTOGEN WRAPPER FUNCTIONS
# ========================================================================
# These functions wrap the async functions from contoso_tools to work with AutoGen
# --- Additional customer service / billing-related wrappers ---  
  
async def get_all_customers() -> str:  
    """List all customers with basic info."""  
    try:  
        customers = await get_all_customers_async()  
        if not customers:  
            return "No customers found."  
        result = "Customer list:\n"  
        for c in customers:  
            result += f"- {c['customer_id']}: {c['first_name']} {c['last_name']} ({c['email']}) - Loyalty: {c['loyalty_level']}\n"  
        return result  
    except Exception as e:  
        return f"Error retrieving customers: {str(e)}"  
  
async def get_customer_orders(customer_id: int) -> str:  
    """List all orders placed by a customer."""  
    try:  
        orders = await get_customer_orders_async(customer_id)  
        if not orders:  
            return f"No orders found for customer {customer_id}"  
        result = f"Orders for customer {customer_id}:\n"  
        for o in orders:  
            result += f"- Order {o['order_id']} on {o['order_date']}: {o['product_name']} (${o['amount']:.2f}) [{o['order_status']}]\n"  
        return result  
    except Exception as e:  
        return f"Error retrieving orders for customer {customer_id}: {str(e)}"  
  
async def get_subscription_detail(subscription_id: int) -> str:  
    """Get detailed subscription info."""  
    try:  
        sub = await get_subscription_detail_async(subscription_id)  
        result = f"Subscription {subscription_id} ({sub['product_name']}):\nStatus: {sub['status']}\n"  
        result += f"Invoices: {len(sub['invoices'])}, Incidents: {len(sub['service_incidents'])}\n"  
        return result  
    except Exception as e:  
        return f"Error retrieving subscription {subscription_id}: {str(e)}"  
  
async def update_subscription(subscription_id: int, updates: dict) -> str:  
    """Update subscription fields."""  
    try:  
        res = await update_subscription_async(subscription_id, updates)  
        return f"Subscription {subscription_id} updated: {', '.join(res['updated_fields'])}"  
    except Exception as e:  
        return f"Error updating subscription {subscription_id}: {str(e)}"  
  
async def get_data_usage(subscription_id: int, start_date: str, end_date: str, aggregate: bool=False) -> str:  
    """Get subscription data usage."""  
    try:  
        usage = await get_data_usage_async(subscription_id, start_date, end_date, aggregate)  
        if aggregate:  
            return f"Total usage: {usage['total_mb']} MB, {usage['total_voice_minutes']} mins, {usage['total_sms']} SMS"  
        else:  
            result = "Daily usage:\n"  
            for u in usage:  
                result += f"{u['usage_date']}: {u['data_used_mb']} MB, {u['voice_minutes']} mins, {u['sms_count']} SMS\n"  
            return result  
    except Exception as e:  
        return f"Error retrieving usage: {str(e)}"  
  
async def get_support_tickets(customer_id: int, open_only: bool=False) -> str:  
    """Get support tickets for a customer."""  
    try:  
        tickets = await get_support_tickets_async(customer_id, open_only)  
        if not tickets:  
            return f"No {'open ' if open_only else ''}tickets for customer {customer_id}"  
        result = f"Support tickets for customer {customer_id}:\n"  
        for t in tickets:  
            result += f"- Ticket {t['ticket_id']} ({t['status']}): {t['subject']}\n"  
        return result  
    except Exception as e:  
        return f"Error retrieving tickets: {str(e)}"  
  
async def create_support_ticket(customer_id: int, subscription_id: int, category: str, priority: str, subject: str, description: str) -> str:  
    """Create a new support ticket."""  
    try:  
        t = await create_support_ticket_async(customer_id, subscription_id, category, priority, subject, description)  
        return f"Ticket {t['ticket_id']} created for customer {customer_id}."  
    except Exception as e:  
        return f"Error creating ticket: {str(e)}"  
async def get_invoice_payments(invoice_id: int) -> str:
    """Get all payments made against a specific invoice. Returns payment history including amounts, dates, and status."""
    try:
        payments = await get_invoice_payments_async(invoice_id)
        if not payments:
            return f"No payments found for invoice {invoice_id}"
        
        result = f"Payments for invoice {invoice_id}:\n"
        for payment in payments:
            result += f"- Payment {payment['payment_id']}: ${payment['amount']:.2f} on {payment['payment_date']} ({payment['status']})\n"
        return result
    except Exception as e:
        return f"Error retrieving payments for invoice {invoice_id}: {str(e)}"

async def pay_invoice(invoice_id: int, amount: float, method: str = "credit_card") -> str:
    """Record a payment against an invoice and get the updated balance. Returns the new outstanding amount."""
    try:
        result = await pay_invoice_async(invoice_id, amount, method)
        outstanding = result.get('outstanding', 0)
        return f"Payment of ${amount:.2f} recorded for invoice {invoice_id}. Outstanding balance: ${outstanding:.2f}"
    except Exception as e:
        return f"Error processing payment for invoice {invoice_id}: {str(e)}"

async def get_billing_summary(customer_id: int) -> str:
    """Get comprehensive billing summary showing what a customer owes across all subscriptions."""
    try:
        summary = await get_billing_summary_async(customer_id)
        total_due = summary.get('total_due', 0)
        invoices = summary.get('invoices', [])
        
        if total_due == 0:
            return f"Customer {customer_id} has no outstanding balance."
        
        result = f"Customer {customer_id} billing summary:\n"
        result += f"Total outstanding: ${total_due:.2f}\n"
        result += "Outstanding invoices:\n"
        for inv in invoices:
            if inv['outstanding'] > 0:
                result += f"- Invoice {inv['invoice_id']}: ${inv['outstanding']:.2f}\n"
        return result
    except Exception as e:
        return f"Error retrieving billing summary for customer {customer_id}: {str(e)}"

async def unlock_account(customer_id: int) -> str:
    """Unlock a customer account that was previously locked for security reasons."""
    try:
        result = await unlock_account_async(customer_id)
        return f"Customer {customer_id} account unlocked successfully. {result.get('message', '')}"
    except Exception as e:
        return f"Error unlocking account for customer {customer_id}: {str(e)}"

async def get_security_logs(customer_id: int) -> str:
    """Get security event history for a customer account, showing recent security activities."""
    try:
        logs = await get_security_logs_async(customer_id)
        if not logs:
            return f"No security events found for customer {customer_id}"
        
        result = f"Security events for customer {customer_id} (most recent first):\n"
        for log in logs[:10]:  # Show last 10 events
            result += f"- {log['event_timestamp']}: {log['event_type']} - {log['description']}\n"
        return result
    except Exception as e:
        return f"Error retrieving security logs for customer {customer_id}: {str(e)}"

async def get_promotions() -> str:
    """Get all active promotions available in the system."""
    try:
        promotions = await get_promotions_async()
        if not promotions:
            return "No active promotions found"
        
        result = "Active promotions:\n"
        for promo in promotions:
            discount = f"{promo['discount_percent']}% off" if promo.get('discount_percent') else "Special offer"
            result += f"- {promo['name']}: {promo['description']} ({discount})\n"
            result += f"  Valid: {promo['start_date']} to {promo['end_date']}\n"
        return result
    except Exception as e:
        return f"Error retrieving promotions: {str(e)}"

async def get_eligible_promotions(customer_id: int) -> str:
    """Get promotions that a specific customer is eligible for based on their loyalty level and current dates."""
    try:
        promotions = await get_eligible_promotions_async(customer_id)
        if not promotions:
            return f"No eligible promotions found for customer {customer_id}"
        
        result = f"Eligible promotions for customer {customer_id}:\n"
        for promo in promotions:
            discount = f"{promo['discount_percent']}% off" if promo.get('discount_percent') else "Special offer"
            result += f"- {promo['name']}: {promo['description']} ({discount})\n"
            result += f"  Valid: {promo['start_date']} to {promo['end_date']}\n"
        return result
    except Exception as e:
        return f"Error retrieving eligible promotions for customer {customer_id}: {str(e)}"

async def get_products(category: str = None) -> str:
    """Get available products, optionally filtered by category (e.g., 'Mobile', 'Internet', 'TV')."""
    try:
        products = await get_products_async(category)
        if not products:
            return f"No products found{' in category ' + category if category else ''}"
        
        result = f"Available products{' in ' + category + ' category' if category else ''}:\n"
        for product in products:
            result += f"- {product['name']} (${product['monthly_fee']:.2f}/month)\n"
            result += f"  {product['description']}\n"
        return result
    except Exception as e:
        return f"Error retrieving products: {str(e)}"

async def get_product_detail(product_id: int) -> str:
    """Get detailed information about a specific product by ID."""
    try:
        product = await get_product_detail_async(product_id)
        result = f"Product {product_id} details:\n"
        result += f"Name: {product['name']}\n"
        result += f"Category: {product['category']}\n"
        result += f"Monthly fee: ${product['monthly_fee']:.2f}\n"
        result += f"Description: {product['description']}\n"
        return result
    except Exception as e:
        return f"Error retrieving product {product_id}: {str(e)}"

# Additional useful functions for customer service

async def search_knowledge_base_func(query: str) -> str:
    """Search the knowledge base for policy and procedure information using natural language queries."""
    try:
        results = await search_knowledge_base_async(query, topk=3)
        if not results:
            return f"No relevant information found for query: {query}"
        
        result = f"Knowledge base search results for '{query}':\n\n"
        for i, doc in enumerate(results, 1):
            result += f"{i}. {doc['title']} ({doc['doc_type']})\n"
            result += f"{doc['content'][:500]}{'...' if len(doc['content']) > 500 else ''}\n\n"
        return result
    except Exception as e:
        return f"Error searching knowledge base: {str(e)}"

async def get_customer_info_func(customer_id: int) -> str:
    """Get comprehensive customer information including profile and subscription details."""
    try:
        customer = await get_customer_detail_async(customer_id)
        result = f"Customer {customer_id} Information:\n"
        result += f"Name: {customer['first_name']} {customer['last_name']}\n"
        result += f"Email: {customer['email']}\n"
        result += f"Phone: {customer.get('phone', 'N/A')}\n"
        result += f"Loyalty Level: {customer['loyalty_level']}\n"
        
        if customer.get('subscriptions'):
            result += f"\nActive Subscriptions ({len(customer['subscriptions'])}):\n"
            for sub in customer['subscriptions']:
                result += f"- Subscription {sub['subscription_id']}: {sub['status']}\n"
        else:
            result += "\nNo active subscriptions found.\n"
        
        return result
    except Exception as e:
        return f"Error retrieving customer {customer_id} information: {str(e)}"  
  
# --- Azure OpenAI + Autogen imports ---  
_autogen_import_error: Exception | None = None  
AssistantAgent = None  
RoundRobinGroupChat = None
TextMessageTermination = None
CancellationToken = None
AzureOpenAIChatCompletionClient = None  
  
try:  
    from autogen_agentchat.agents import AssistantAgent as _AA
    from autogen_agentchat.teams import RoundRobinGroupChat as _RRG
    from autogen_agentchat.conditions import TextMessageTermination as _TMT
    from autogen_core import CancellationToken as _CT
    AssistantAgent = _AA  
    RoundRobinGroupChat = _RRG
    TextMessageTermination = _TMT
    CancellationToken = _CT
except Exception as e:  
    _autogen_import_error = e  
  
if AzureOpenAIChatCompletionClient is None:  
    try:  
        from autogen_ext.models.openai import AzureOpenAIChatCompletionClient as _AzureClient  
        AzureOpenAIChatCompletionClient = _AzureClient  
    except Exception as e:  
        _autogen_import_error = e  
  
if (AssistantAgent is None or RoundRobinGroupChat is None or 
    TextMessageTermination is None or CancellationToken is None or 
    AzureOpenAIChatCompletionClient is None):  
    raise RuntimeError(  
        "Autogen with AzureOpenAIChatCompletionClient, AssistantAgent, and RoundRobinGroupChat is required. "  
        f"Last import error: {_autogen_import_error}"  
    )  
  
# --- Required environment variables ---  
AZURE_OPENAI_CHAT_DEPLOYMENT = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")  
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")  
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")  
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")  
MCP_SERVER_URI = os.getenv("MCP_SERVER_URI")  
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")  
  
if not AZURE_OPENAI_CHAT_DEPLOYMENT:  
    raise RuntimeError("AZURE_OPENAI_CHAT_DEPLOYMENT is not set")  
if not AZURE_OPENAI_API_KEY:  
    raise RuntimeError("AZURE_OPENAI_API_KEY is not set")  
if not AZURE_OPENAI_ENDPOINT:  
    raise RuntimeError("AZURE_OPENAI_ENDPOINT is not set")  
if not AZURE_OPENAI_API_VERSION:  
    raise RuntimeError("AZURE_OPENAI_API_VERSION is not set")  
  
# --- Domains ---  
DOMAIN_BILLING = "invoice_payment"  
DOMAIN_ACCOUNT = "account_login"  
DOMAIN_PRODUCT = "product_promotions"  
  
# --- Models ---  
@dataclass  
class AgentTurn:  
    role: str  
    content: str  
    ts: float = field(default_factory=time.time)  
  
@dataclass  
class AgentRunResult:  
    status: str  # "done" | "needs_input" | "error"  
    messages: list[AgentTurn]  
    result: Any | None = None  
    error: str | None = None  
  
# --- Load tools based on domain ---  
def load_domain_tools(domain: str) -> list[Any]:  
    try:  
        if domain == DOMAIN_BILLING:  
            return [  
                # Existing billing tools  
                get_invoice_payments,  
                pay_invoice,  
                get_billing_summary,  
  
                get_all_customers,  
                get_customer_info_func,  
                get_customer_orders,  
                get_subscription_detail,  
                update_subscription,  
                get_data_usage,  
                get_support_tickets,  
                create_support_ticket  
            ]  
        elif domain == DOMAIN_ACCOUNT:  
            return [  
                unlock_account,  
                get_security_logs,
                get_all_customers,  
                get_customer_info_func,  
                get_customer_orders,  
                get_subscription_detail,  
                update_subscription,  
                get_data_usage,  
                get_support_tickets,  
                create_support_ticket  
  
            ]  
        elif domain == DOMAIN_PRODUCT:  
            return [  
                get_promotions,  
                get_eligible_promotions,  
                get_products,  
                get_product_detail,
                get_all_customers,  
                get_customer_info_func,  
                get_customer_orders,  
                get_subscription_detail,  
                update_subscription,  
                get_data_usage,  
                get_support_tickets,  
                create_support_ticket  
  
            ]  
        else:  
            return []  
    except Exception:  
        return []    
# --- Domain Agent ---  
class DomainAgent:  
    def __init__(self, domain: str, temperature: float = 0.2, model_name: str | None = OPENAI_MODEL_NAME):  
        self.domain = domain  
        self.temperature = float(temperature or 0.2)  
        self.model_name = model_name or "azure-openai-gpt"  
        self.history: list[AgentTurn] = []  
        self.loop_agent = None
        self._initialized = False
        self.state = None

        self.model_client = AzureOpenAIChatCompletionClient(  
            api_key=AZURE_OPENAI_API_KEY,  
            azure_endpoint=AZURE_OPENAI_ENDPOINT,  
            api_version=AZURE_OPENAI_API_VERSION,  
            azure_deployment=AZURE_OPENAI_CHAT_DEPLOYMENT,  
            model=self.model_name,  
        )  

    async def _setup_loop_agent(self) -> None:
        """Initialize the assistant and loop agent once."""
        if self._initialized:
            return

        tools = load_domain_tools(self.domain)
        
        # Set up the assistant agent  
        agent = AssistantAgent(  
            name=f"{self.domain}_assistant",  
            model_client=self.model_client,  
            tools=tools,  
            system_message=self._system_prompt_for(),  
        )  

        # Set the termination condition: stop when agent answers as itself  
        termination_condition = TextMessageTermination(f"{self.domain}_assistant")  

        self.loop_agent = RoundRobinGroupChat(  
            [agent],  
            termination_condition=termination_condition,  
        )  

        if self.state:  
            await self.loop_agent.load_state(self.state)  
        self._initialized = True

    def _system_prompt_for(self) -> str:  
        shared_contract = (  
            "You are a helpful assistant. You can use multiple tools to find information and answer questions. "  
            "Review the tools available to you and use them as needed. You can also ask clarifying questions if "  
            "the user is not clear. "  
            "Never hallucinate any operation that you do not actually do.\n"  
        )  
    
        if self.domain == DOMAIN_BILLING:  
            return (  
                "You are an expert assistant for all customer account and billing-related matters. "  
                "You can handle invoices, payments, billing summaries, customer profile lookups, subscription details and updates, "  
                "order history, data usage reports, and support ticket creation or retrieval. "  
                "You can answer questions that combine any of these areas.\n"  
                + shared_contract  
            )  
    
        if self.domain == DOMAIN_ACCOUNT:  
            return (  
                "You are an expert in account access and security issues. "  
                "You can unlock locked accounts, review and explain recent security logs, "  
                "and assist with account-related security events.\n"  
                + shared_contract  
            )  
    
        if self.domain == DOMAIN_PRODUCT:  
            return (  
                "You are an expert on the product catalog and promotions. "  
                "You can list available products, filter by category, retrieve product details, "  
                "and find promotions (including those that a specific customer is eligible for) based on loyalty level and dates.\n"  
                + shared_contract  
            )  
    
        return "You are a helpful domain expert.\n" + shared_contract  
    def _parse_status(self, assistant_text: str) -> tuple[str, Any | None]:  
        for ln in assistant_text.splitlines():  
            s = ln.strip()  
            if s.lower().startswith("final:"):  
                return "done", s[6:].strip()  
        return "needs_input", None

    async def run_turn(self, user_input: Optional[str], max_steps: int = 6) -> AgentRunResult:
        """Run a conversation turn using the loop agent pattern with state persistence."""
        messages: list[AgentTurn] = []
        try:
            # Ensure agent/tools are ready
            await self._setup_loop_agent()

            if user_input:
                messages.append(AgentTurn(role="user", content=user_input))

            # Run the loop agent
            response = await self.loop_agent.run(task=user_input or "continue", cancellation_token=CancellationToken())
            assistant_text = response.messages[-1].content

            messages.append(AgentTurn(role="assistant", content=assistant_text))
            self.history.extend(messages)

            # Update/store latest agent state  
            new_state = await self.loop_agent.save_state()
            self.state = new_state

            status, final = self._parse_status(assistant_text)
            if status == "done":
                return AgentRunResult(status="done", messages=messages, result=final)
            return AgentRunResult(status="needs_input", messages=messages)
        except Exception as e:
            return AgentRunResult(status="error", messages=messages, error=str(e))  
  
# --- Agents Manager ---  
class AgentsManager:  
    def __init__(self):  
        self._by_session: dict[str, dict[str, DomainAgent]] = {}  
        self._locks: dict[str, asyncio.Lock] = {}
        # State store for persistent state management like BaseAgent
        self._state_store: dict[str, Any] = {}

    def lock_for(self, session_id: str) -> asyncio.Lock:  
        if session_id not in self._locks:  
            self._locks[session_id] = asyncio.Lock()  
        return self._locks[session_id]  

    def _get_bucket(self, session_id: str) -> dict[str, DomainAgent]:  
        return self._by_session.setdefault(session_id, {})  

    def get_or_create(self, session_id: str, domain: str, temperature: float = 0.2, model_name: str | None = OPENAI_MODEL_NAME) -> DomainAgent:  
        bucket = self._get_bucket(session_id)  
        if domain not in bucket:  
            agent = DomainAgent(domain=domain, temperature=temperature, model_name=model_name)
            # Load existing state if available
            state_key = f"{session_id}_{domain}"
            if state_key in self._state_store:
                agent.state = self._state_store[state_key]
            bucket[domain] = agent
        return bucket[domain]

    def save_agent_state(self, session_id: str, domain: str, state: Any) -> None:
        """Save agent state for persistence across conversations."""
        state_key = f"{session_id}_{domain}"
        self._state_store[state_key] = state

    def reset_session(self, session_id: str) -> None:  
        # Clear session agents but preserve state for potential recovery
        self._by_session.pop(session_id, None)  
        self._locks.pop(session_id, None)
        # Optionally clear state store keys for this session
        # keys_to_remove = [k for k in self._state_store.keys() if k.startswith(f"{session_id}_")]
        # for key in keys_to_remove:
        #     self._state_store.pop(key, None)

AGENTS = AgentsManager()  
  
# --- FastMCP server setup ---  
server = FastMCP(name="Agentic MCP (Azure OpenAI + Autogen)", sampling_handler_behavior="fallback")  
server.add_middleware(ErrorHandlingMiddleware(include_traceback=False))  
server.add_middleware(LoggingMiddleware(include_payloads=False))  
server.add_middleware(TimingMiddleware())  
  
# async def _register_session_cleanup(ctx: Context) -> None:  
#     async def cleanup():  
#         AGENTS.reset_session(ctx.session_id)  
#     try:  
#         ctx.session._exit_stack.push_async_callback(cleanup)  # type: ignore[attr-defined]  
#     except Exception:  
#         pass  
  
async def _run_domain_tool(*, ctx: Context, domain: str, input: str) -> dict:  
    # await _register_session_cleanup(ctx)  
    session_id = ctx.session_id  
    lock = AGENTS.lock_for(session_id)  
    async with lock:  
        agent = AGENTS.get_or_create(  
            session_id=session_id,  
            domain=domain,  
            temperature=0.2,  
            model_name=OPENAI_MODEL_NAME,  
        )  
        result = await agent.run_turn(user_input=input)
        print("result ", result)
        
        # Save agent state for multi-turn conversation support
        if agent.state:
            AGENTS.save_agent_state(session_id, domain, agent.state)
        
        return {  
            "domain": domain,  
            "status": result.status,  
            "messages": [t.__dict__ for t in result.messages],  
            "result": result.result,  
            "error": result.error,  
        }  
  
# --- High-level tools ---  
@server.tool(name="ask_billing_expert", description="Consult the billing/invoice/payment expert.", tags={"billing", "invoice", "payment"})  
async def ask_billing_expert(question: str, ctx: Context | None = None) -> dict:  
    assert ctx is not None  
    return await _run_domain_tool(ctx=ctx, domain=DOMAIN_BILLING, input=question)  
  
@server.tool(name="ask_account_expert", description="Consult the account-access expert.", tags={"account", "login", "mfa"})  
async def ask_account_expert(question: str, ctx: Context | None = None) -> dict:  
    assert ctx is not None  
    return await _run_domain_tool(ctx=ctx, domain=DOMAIN_ACCOUNT, input=question)  
  
@server.tool(name="ask_product_expert", description="Consult the product & promotions expert.", tags={"product", "promotions", "catalog"})  
async def ask_product_expert(question: str, ctx: Context | None = None) -> dict:  
    assert ctx is not None  
    return await _run_domain_tool(ctx=ctx, domain=DOMAIN_PRODUCT, input=question)  
from fastmcp.server import Context
import asyncio


# --- Entrypoint ---  
if __name__ == "__main__":  
    asyncio.run(server.run_http_async(host="0.0.0.0", port=8000))  