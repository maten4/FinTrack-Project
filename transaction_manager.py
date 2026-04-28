"""
transaction_manager.py
Load, save, view add, and remove transactions.
"""

from datetime import datetime
from data_manager import load_data, save_data


def view_all_transactions():
    data = load_data()
    txns = data.get("transactions", [])
    if not txns:
        print("  No transactions found.")
        return
    print(f"\n  {'ID':<8} {'Date':<12} {'Type':<16} {'Amount':>8}  Description")
    print("  " + "-" * 62)
    for t in txns:
        # Income gets a + prefix, everything else gets a minus
        sign = "+" if t["type"] == "income" else "-"
        print(f"  {t['id']:<8} {t['date']:<12} {t['type']:<16} {sign}£{t['amount']:>6.2f}  {t['description']}")
    print(f"\n  Current Balance: £{data['current_balance']:.2f}")

 
def view_transactions_by_type(txn_type):
        # Filter down to just the type the caller asked for (e.g. "income" or "expense")
    data = load_data()
    txns = [t for t in data["transactions"] if t["type"] == txn_type]
    if not txns:
        print(f"  No '{txn_type}' transactions found.")
        return
    print(f"\n  {'ID':<8} {'Date':<12} {'Amount':>8}  Description")
    print("  " + "-" * 48)
    for t in txns:
        print(f"  {t['id']:<8} {t['date']:<12} £{t['amount']:>6.2f}  {t['description']}")


def _next_id(txns):
    # Generate the next TXN ID based on the highest existing number
    nums = [int(t["id"].replace("TXN", "")) for t in txns if t["id"].startswith("TXN")]
    return f"TXN{(max(nums) + 1 if nums else 1):03d}"
 
def _today():
    # Just a small helper so we're not repeating this format string everywhere
    return datetime.today().strftime("%Y-%m-%d")


def add_income(description, amount, source, is_taxable=True, date=None):
    data = load_data()
    txn = {"id": _next_id(data["transactions"]), "type": "income",
           "date": date or _today(), "amount": round(float(amount), 2),
           "description": description, "source": source, "is_taxable": is_taxable} # handy to track for self-assessment later
    data["transactions"].append(txn)
    data["current_balance"] = round(data["current_balance"] + txn["amount"], 2)
    save_data(data)
    print(f"  Income '{description}' (£{amount:.2f}) added as {txn['id']}.")

 
def add_expense(description, amount, category, importance="Need", date=None):
    data = load_data()
    txn = {"id": _next_id(data["transactions"]), "type": "expense",
           "date": date or _today(), "amount": round(float(amount), 2),
           "description": description, "category": category, "importance": importance} # "Need" vs "Want" — useful for budget reviews
    data["transactions"].append(txn)
    data["current_balance"] = round(data["current_balance"] - txn["amount"], 2)
    save_data(data)
    print(f"  Expense '{description}' (£{amount:.2f}) added as {txn['id']}.")

 
def add_recurring_bill(description, amount, category, importance="Need", frequency="monthly", date=None):
    data = load_data()
    today = datetime.today()
    # Calculate next due date by bumping the month forward by one
    next_month = today.month % 12 + 1
    next_year = today.year + (1 if today.month == 12 else 0)
    txn = {"id": _next_id(data["transactions"]), "type": "recurring_bill",
           "date": date or _today(), "amount": round(float(amount), 2),
           "description": description, "category": category, "importance": importance,
           "frequency": frequency, "next_due_date": f"{next_year}-{next_month:02d}-{today.day:02d}"}
    data["transactions"].append(txn)
    data["current_balance"] = round(data["current_balance"] - txn["amount"], 2)
    save_data(data)
    print(f"  Recurring bill '{description}' (£{amount:.2f}) added as {txn['id']}.")

# --- Remove ---

def remove_transaction(txn_id):
    data = load_data()
    target = next((t for t in data["transactions"] if t["id"] == txn_id), None)
    if not target:
        print(f"  Transaction '{txn_id}' not found.")
        return
    # Reverse the balance effect before removing
    if target["type"] == "income":
        data["current_balance"] = round(data["current_balance"] - target["amount"], 2)
    else:
        data["current_balance"] = round(data["current_balance"] + target["amount"], 2)
    data["transactions"] = [t for t in data["transactions"] if t["id"] != txn_id]
    save_data(data)
    print(f"  Removed '{txn_id}' ({target['description']}).")

# --- Summary ---
 
def get_summary():
    data = load_data()
    income   = sum(t["amount"] for t in data["transactions"] if t["type"] == "income")
    expenses = sum(t["amount"] for t in data["transactions"] if t["type"] in ("expense", "recurring_bill"))
    return {"total_income": round(income, 2), "total_expenses": round(expenses, 2),
            "net": round(income - expenses, 2), "balance": data["current_balance"]}