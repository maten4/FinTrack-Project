"""
budget_manager.py
Budget tracking, needs vs wants, alerts, nad upcoming bills.
"""

from data_manager import load_data, save_data

def get_spending_by_category():
    # tally all outgoing transactions grouped by category
    data = load_data()
    spending = {}
    for t in data["transactions"]:
        if t["type"] in ("expense", "recurring_bill"):
            cat = t.get("category", "Uncategorised")
            spending[cat] = round(spending.get(cat, 0.0) + t["amount"], 2)
    return spending
 
 
# --- Budget Alerts ---
 
def check_budget_alerts():
    data = load_data()
    spending = get_spending_by_category()
    print("\n  -- Budget Alerts --")
    for cat, limit in data.get("budgets", {}).items():
        spent = spending.get(cat, 0.0)
        pct = (spent / limit * 100) if limit > 0 else 0
        status = "OVER BUDGET" if pct >= 100 else ("nearing limit" if pct >= 80 else "OK")
        print(f"  {cat:<16} £{spent:.2f} / £{limit:.2f}  ({pct:.0f}%)  {status}")
    print()
 
def view_budget_summary():
    data = load_data()
    spending = get_spending_by_category()
    print(f"\n  {'Category':<16} {'Budget':>8}  {'Spent':>8}  {'Remaining':>10}")
    print("  " + "-" * 48)
    for cat, limit in data.get("budgets", {}).items():
        remaining = limit - spending.get(cat, 0.0)
        # Show negative remaining in brackets to make overspend obvious
        rem_str = f"£{remaining:.2f}" if remaining >= 0 else f"(£{abs(remaining):.2f})"
        print(f"  {cat:<16} £{limit:>6.2f}  £{spending.get(cat, 0.0):>6.2f}  {rem_str:>10}")
    print()
 
def set_budget(category, amount):
    data = load_data()
    data["budgets"][category] = round(float(amount), 2)
    save_data(data)
    print(f"  Budget for '{category}' set to £{amount:.2f}.")
 
 
# --- Needs vs Wants ---
 
def needs_vs_wants_breakdown():
    data = load_data()
    needs, wants = [], []
    for t in data["transactions"]:
        if t["type"] in ("expense", "recurring_bill"):
            (needs if t.get("importance") == "Need" else wants).append(t)
 
    needs_total = sum(t["amount"] for t in needs)
    wants_total = sum(t["amount"] for t in wants)
    grand_total = needs_total + wants_total
 
    print("\n  -- Needs vs. Wants --")
    print(f"\n  NEEDS  £{needs_total:.2f}")
    for t in needs:
        print(f"    {t['description']:<25} £{t['amount']:.2f}")
    print(f"\n  WANTS  £{wants_total:.2f}")
    for t in wants:
        print(f"    {t['description']:<25} £{t['amount']:.2f}")
 
    if grand_total > 0:
        needs_pct = needs_total / grand_total * 100
        bar_width = 50
        n = round(needs_pct / 100 * bar_width)
        print(f"\n  Needs {needs_pct:.1f}%  |  Wants {100 - needs_pct:.1f}%")
        print(f"  [{'#' * n}{'-' * (bar_width - n)}]")
    print()
 
 
# --- Upcoming Bills ---
 
def upcoming_bills():
    data = load_data()
    bills = sorted(
        [t for t in data["transactions"] if t["type"] == "recurring_bill"],
        key=lambda b: b.get("next_due_date", "9999-12-31")
    )
    if not bills:
        print("  No recurring bills found.")
        return
    print(f"\n  -- Upcoming Bills --")
    print(f"  {'Description':<25} {'Amount':>8}  Next Due")
    print("  " + "-" * 46)
    for b in bills:
        print(f"  {b['description']:<25} £{b['amount']:>6.2f}  {b.get('next_due_date', 'N/A')}")
    print()