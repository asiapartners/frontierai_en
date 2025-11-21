"""Contoso Customer Service Utility Module  
  
Provides granular async functions for interacting with the Contoso  
customer database. Designed to be used by both MCP tools and AutoGen  
agents.  
"""  
  
import os  
import json  
import math  
import sqlite3  
from typing import List, Optional, Dict, Any  
from datetime import datetime  
from dotenv import load_dotenv  
  
# Load environment variables  
load_dotenv()  
  
# Database configuration  
DB_PATH = os.getenv("DB_PATH", "data/contoso.db")  
  
  
def get_db() -> sqlite3.Connection:  
    """Get a database connection with row factory."""  
    db = sqlite3.connect(DB_PATH)  
    db.row_factory = sqlite3.Row  
    return db  
  
  
# Safe OpenAI import / dummy embedding  
try:  
    from openai import AzureOpenAI  
  
    _client = AzureOpenAI(  
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),  
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),  
    )  
    _emb_model = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")  
  
    def get_embedding(text: str) -> List[float]:  
        """Get embedding vector from Azure OpenAI."""  
        text = text.replace("\n", " ")  
        return _client.embeddings.create(input=[text], model=_emb_model).data[0].embedding  
  
except Exception:  
    def get_embedding(text: str) -> List[float]:  
        """Fallback to zero vector when credentials are missing."""  
        return [0.0] * 1536  
  
  
def cosine_similarity(vec1, vec2):  
    """Calculate cosine similarity between two vectors."""  
    dot = sum(a * b for a, b in zip(vec1, vec2))  
    norm1 = math.sqrt(sum(a * a for a in vec1))  
    norm2 = math.sqrt(sum(b * b for b in vec2))  
    return dot / (norm1 * norm2) if norm1 and norm2 else 0.0  
  
  
# ========================================================================  
# CUSTOMER FUNCTIONS  
# ========================================================================  
  
async def get_all_customers_async() -> List[Dict[str, Any]]:  
    db = get_db()  
    rows = db.execute(  
        "SELECT customer_id, first_name, last_name, email, loyalty_level FROM Customers"  
    ).fetchall()  
    db.close()  
    return [dict(r) for r in rows]  
  
  
async def get_customer_detail_async(customer_id: int) -> Dict[str, Any]:  
    db = get_db()  
    cust = db.execute(  
        "SELECT * FROM Customers WHERE customer_id = ?", (customer_id,)  
    ).fetchone()  
    if not cust:  
        db.close()  
        raise ValueError(f"Customer {customer_id} not found")  
    subs = db.execute(  
        "SELECT * FROM Subscriptions WHERE customer_id = ?", (customer_id,)  
    ).fetchall()  
    db.close()  
    result = dict(cust)  
    result['subscriptions'] = [dict(s) for s in subs]  
    return result  
  
  
async def get_customer_orders_async(customer_id: int) -> List[Dict[str, Any]]:  
    db = get_db()  
    rows = db.execute(  
        """SELECT o.order_id, o.order_date, p.name as product_name,  
                  o.amount, o.order_status  
           FROM Orders o  
           JOIN Products p ON p.product_id = o.product_id  
           WHERE o.customer_id = ?  
           ORDER BY o.order_date DESC""",  
        (customer_id,),  
    ).fetchall()  
    db.close()  
    return [dict(r) for r in rows]  
  
  
# ========================================================================  
# SUBSCRIPTION FUNCTIONS  
# ========================================================================  
  
async def get_subscription_detail_async(subscription_id: int) -> Dict[str, Any]:  
    db = get_db()  
    sub = db.execute(  
        """SELECT s.*, p.name AS product_name, p.description AS product_description,  
                  p.category, p.monthly_fee  
           FROM Subscriptions s  
           JOIN Products p ON p.product_id = s.product_id  
           WHERE s.subscription_id = ?""",  
        (subscription_id,),  
    ).fetchone()  
    if not sub:  
        db.close()  
        raise ValueError("Subscription not found")  
  
    invoices_rows = db.execute(  
        "SELECT invoice_id, invoice_date, amount, description, due_date "  
        "FROM Invoices WHERE subscription_id = ?",  
        (subscription_id,),  
    ).fetchall()  
  
    invoices = []  
    for inv in invoices_rows:  
        pay_rows = db.execute(  
            "SELECT * FROM Payments WHERE invoice_id = ?", (inv["invoice_id"],)  
        ).fetchall()  
        total_paid = sum(p["amount"] for p in pay_rows if p["status"] == "successful")  
        invoice_dict = dict(inv)  
        invoice_dict['payments'] = [dict(p) for p in pay_rows]  
        invoice_dict['outstanding'] = max(inv["amount"] - total_paid, 0.0)  
        invoices.append(invoice_dict)  
  
    inc_rows = db.execute(  
        "SELECT incident_id, incident_date, description, resolution_status "  
        "FROM ServiceIncidents WHERE subscription_id = ?",  
        (subscription_id,),  
    ).fetchall()  
    db.close()  
  
    result = dict(sub)  
    result['invoices'] = invoices  
    result['service_incidents'] = [dict(r) for r in inc_rows]  
    return result  
  
  
async def update_subscription_async(subscription_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:  
    if not updates:  
        raise ValueError("No fields supplied")  
    data = {k: v for k, v in updates.items() if v is not None}  
    if not data:  
        raise ValueError("No valid fields to update")  
  
    sets = ", ".join(f"{k} = ?" for k in data)  
    params = list(data.values()) + [subscription_id]  
  
    db = get_db()  
    cur = db.execute(f"UPDATE Subscriptions SET {sets} WHERE subscription_id = ?", params)  
    db.commit()  
    db.close()  
  
    if cur.rowcount == 0:  
        raise ValueError("Subscription not found")  
    return {"subscription_id": subscription_id, "updated_fields": list(data.keys())}  
  
  
async def get_data_usage_async(subscription_id: int, start_date: str, end_date: str, aggregate: bool = False) -> List[Dict[str, Any]] | Dict[str, Any]:  
    db = get_db()  
    rows = db.execute(  
        """SELECT usage_date, data_used_mb, voice_minutes, sms_count  
           FROM DataUsage  
           WHERE subscription_id = ?  
             AND usage_date BETWEEN ? AND ?  
           ORDER BY usage_date""",  
        (subscription_id, start_date, end_date),  
    ).fetchall()  
    db.close()  
  
    if aggregate:  
        return {  
            "subscription_id": subscription_id,  
            "start_date": start_date,  
            "end_date": end_date,  
            "total_mb": sum(r["data_used_mb"] for r in rows),  
            "total_voice_minutes": sum(r["voice_minutes"] for r in rows),  
            "total_sms": sum(r["sms_count"] for r in rows),  
        }  
    return [dict(r) for r in rows]  
  
  
# ========================================================================  
# BILLING FUNCTIONS  
# ========================================================================  
  
async def get_billing_summary_async(customer_id: int) -> Dict[str, Any]:  
    db = get_db()  
    inv_rows = db.execute(  
        """SELECT inv.invoice_id, inv.amount,  
                  IFNULL(SUM(pay.amount), 0) AS paid  
           FROM Invoices inv  
           LEFT JOIN Payments pay  
             ON pay.invoice_id = inv.invoice_id AND pay.status='successful'  
           WHERE inv.subscription_id IN  
               (SELECT subscription_id FROM Subscriptions WHERE customer_id = ?)  
           GROUP BY inv.invoice_id""",  
        (customer_id,),  
    ).fetchall()  
    db.close()  
  
    outstanding = [  
        {"invoice_id": r["invoice_id"], "outstanding": max(r["amount"] - r["paid"], 0.0)}  
        for r in inv_rows  
    ]  
    total_due = sum(item["outstanding"] for item in outstanding)  
    return {"customer_id": customer_id, "total_due": total_due, "invoices": outstanding}  
  
  
async def get_invoice_payments_async(invoice_id: int) -> List[Dict[str, Any]]:  
    db = get_db()  
    rows = db.execute("SELECT * FROM Payments WHERE invoice_id = ?", (invoice_id,)).fetchall()  
    db.close()  
    return [dict(r) for r in rows]  
  
  
async def pay_invoice_async(invoice_id: int, amount: float, method: str = "credit_card") -> Dict[str, Any]:  
    today = datetime.now().strftime("%Y-%m-%d")  
    db = get_db()  
    db.execute(  
        "INSERT INTO Payments(invoice_id, payment_date, amount, method, status) VALUES (?,?,?,?,?)",  
        (invoice_id, today, amount, method, "successful"),  
    )  
    inv = db.execute("SELECT amount FROM Invoices WHERE invoice_id = ?", (invoice_id,)).fetchone()  
    if not inv:  
        db.close()  
        raise ValueError("Invoice not found")  
    paid = db.execute(  
        "SELECT SUM(amount) as paid FROM Payments WHERE invoice_id = ? AND status='successful'",  
        (invoice_id,),  
    ).fetchone()["paid"]  
    db.commit()  
    db.close()  
    return {"invoice_id": invoice_id, "outstanding": max(inv["amount"] - (paid or 0), 0.0)}  
  
  
# ========================================================================  
# SECURITY FUNCTIONS  
# ========================================================================  
  
async def get_security_logs_async(customer_id: int) -> List[Dict[str, Any]]:  
    db = get_db()  
    rows = db.execute(  
        "SELECT log_id, event_type, event_timestamp, description "  
        "FROM SecurityLogs WHERE customer_id = ? ORDER BY event_timestamp DESC",  
        (customer_id,),  
    ).fetchall()  
    db.close()  
    return [dict(r) for r in rows]  
  
  
async def unlock_account_async(customer_id: int) -> Dict[str, str]:  
    db = get_db()  
    row = db.execute(  
        "SELECT 1 FROM SecurityLogs WHERE customer_id = ? AND event_type = 'account_locked' "  
        "ORDER BY event_timestamp DESC LIMIT 1",  
        (customer_id,),  
    ).fetchone()  
    if not row:  
        db.close()  
        raise ValueError("No recent lock event; nothing to do.")  
    db.execute(  
        "INSERT INTO SecurityLogs (customer_id, event_type, event_timestamp, description) "  
        "VALUES (?, 'account_unlocked', ?, 'Unlocked via API')",  
        (customer_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),  
    )  
    db.commit()  
    db.close()  
    return {"message": "Account unlocked"}  
  
  
# ========================================================================  
# PRODUCT FUNCTIONS  
# ========================================================================  
  
async def get_products_async(category: Optional[str] = None) -> List[Dict[str, Any]]:  
    db = get_db()  
    if category:  
        rows = db.execute("SELECT * FROM Products WHERE category = ?", (category,)).fetchall()  
    else:  
        rows = db.execute("SELECT * FROM Products").fetchall()  
    db.close()  
    return [dict(r) for r in rows]  
  
  
async def get_product_detail_async(product_id: int) -> Dict[str, Any]:  
    db = get_db()  
    r = db.execute("SELECT * FROM Products WHERE product_id = ?", (product_id,)).fetchone()  
    db.close()  
    if not r:  
        raise ValueError("Product not found")  
    return dict(r)  
  
  
# ========================================================================  
# PROMOTION FUNCTIONS  
# ========================================================================  
  
async def get_promotions_async() -> List[Dict[str, Any]]:  
    db = get_db()  
    rows = db.execute("SELECT * FROM Promotions").fetchall()  
    db.close()  
    return [dict(r) for r in rows]  
  
  
async def get_eligible_promotions_async(customer_id: int) -> List[Dict[str, Any]]:  
    db = get_db()  
    cust = db.execute("SELECT loyalty_level FROM Customers WHERE customer_id = ?", (customer_id,)).fetchone()  
    if not cust:  
        db.close()  
        raise ValueError("Customer not found")  
    loyalty = cust["loyalty_level"]  
    today = datetime.now().strftime("%Y-%m-%d")  
    rows = db.execute(  
        "SELECT * FROM Promotions WHERE start_date <= ? AND end_date >= ?",  
        (today, today),  
    ).fetchall()  
    db.close()  
  
    eligible = []  
    for r in rows:  
        crit = r["eligibility_criteria"] or ""  
        if f"loyalty_level = '{loyalty}'" in crit or "loyalty_level" not in crit:  
            eligible.append(dict(r))  
    return eligible  
  
  
# ========================================================================  
# SUPPORT FUNCTIONS  
# ========================================================================  
  
async def get_support_tickets_async(customer_id: int, open_only: bool = False) -> List[Dict[str, Any]]:  
    db = get_db()  
    query = "SELECT * FROM SupportTickets WHERE customer_id = ?"  
    if open_only:  
        query += " AND status != 'closed'"  
    rows = db.execute(query, (customer_id,)).fetchall()  
    db.close()  
    return [dict(r) for r in rows]  
  
  
async def create_support_ticket_async(customer_id: int, subscription_id: int, category: str, priority: str, subject: str, description: str) -> Dict[str, Any]:  
    opened = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
    db = get_db()  
    cur = db.execute(  
        """INSERT INTO SupportTickets  
           (customer_id, subscription_id, category, opened_at, closed_at,  
            status, priority, subject, description, cs_agent)  
           VALUES (?,?,?,?,?,?,?,?,?,?)""",  
        (customer_id, subscription_id, category, opened, None, "open", priority, subject, description, "AI_Bot"),  
    )  
    ticket_id = cur.lastrowid  
    db.commit()  
    row = db.execute("SELECT * FROM SupportTickets WHERE ticket_id = ?", (ticket_id,)).fetchone()  
    db.close()  
    return dict(row)  
  
  
# ========================================================================  
# KNOWLEDGE BASE FUNCTIONS  
# ========================================================================  
  
async def search_knowledge_base_async(query: str, topk: int = 3) -> List[Dict[str, Any]]:  
    query_emb = get_embedding(query)  
    db = get_db()  
    rows = db.execute("SELECT title, doc_type, content, topic_embedding FROM KnowledgeDocuments").fetchall()  
    db.close()  
  
    scored = []  
    for r in rows:  
        try:  
            emb = json.loads(r["topic_embedding"])  
            sim = cosine_similarity(query_emb, emb)  
            scored.append((sim, r))  
        except Exception:  
            continue  
    scored.sort(reverse=True, key=lambda x: x[0])  
  
    best = scored[:topk]  
    return [{"title": r["title"], "doc_type": r["doc_type"], "content": r["content"]} for _, r in best]  