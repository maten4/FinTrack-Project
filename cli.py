"""
cli.py
Main entry point for FinTrack.
Provides all menus, user input prompts, and the spending histogram.
Run with:  python cli.py
"""
 
from transaction_manager import (
    view_all_transactions,
    view_transactions_by_type,
    add_income,
    add_expense,
    add_recurring_bill,
    remove_transaction,
    get_summary,
)
from budget_manager import (
    check_budget_alerts,
    view_budget_summary,
    needs_vs_wants_breakdown,
    upcoming_bills,
    set_budget,
    get_spending_by_category,
)
 
 
# ─────────────────────────────────────────────
#  HELPER: SAFE INPUT
# ─────────────────────────────────────────────
 
def ask_float(prompt):
    """Keep prompting until the user enters a valid positive number."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("  Please enter a number greater than 0.")
                continue
            return value
        except ValueError:
            print("  Invalid input — please enter a number (e.g. 12.50).")
 
 
def ask_choice(prompt, valid_options):
    """Keep prompting until the user picks one of the valid options."""
    options_str = "/".join(valid_options)
    while True:
        choice = input(f"{prompt} [{options_str}]: ").strip()
        if choice in valid_options:
            return choice
        print(f"  Please enter one of: {options_str}")
 
 
# ─────────────────────────────────────────────
#  HISTOGRAM: SPENDING BY CATEGORY
# ─────────────────────────────────────────────
 
def display_spending_histogram():
    """
    Draw a horizontal ASCII bar chart showing spending per category.
    Bars are scaled so the highest-spend category fills 40 chars.
    """
    spending = get_spending_by_category()
 
    if not spending:
        print("  No spending data to display.")
        return
 
    print("\n  ── Spending Histogram ──────────────────────")
 
    max_amount = max(spending.values())
    bar_max = 40  # maximum bar width in characters
 
    for category, amount in sorted(spending.items(), key=lambda x: -x[1]):
        # Scale the bar length relative to the biggest spender
        bar_len = round((amount / max_amount) * bar_max) if max_amount > 0 else 0
        bar = "█" * bar_len
        print(f"  {category:<16} {bar:<40}  £{amount:.2f}")
 
    print()
 
 
# ─────────────────────────────────────────────
#  SUB-MENUS
# ─────────────────────────────────────────────
 
def menu_view_transactions():
    """Sub-menu: choose how to view transactions."""
    print("\n  View Transactions")
    print("  1. All transactions")
    print("  2. Income only")
    print("  3. Expenses only")
    print("  4. Recurring bills only")
    print("  0. Back")
 
    choice = input("\n  Choice: ").strip()
 
    if choice == "1":
        view_all_transactions()
    elif choice == "2":
        view_transactions_by_type("income")
    elif choice == "3":
        view_transactions_by_type("expense")
    elif choice == "4":
        view_transactions_by_type("recurring_bill")
    elif choice == "0":
        return
    else:
        print("  Invalid option.")
 
 
def menu_add_transaction():
    """Sub-menu: collect details to add a new transaction of any type."""
    print("\n  Add Transaction")
    print("  1. Income")
    print("  2. Expense")
    print("  3. Recurring Bill")
    print("  0. Back")
 
    choice = input("\n  Choice: ").strip()
 
    if choice == "1":
        # Collect income details
        desc = input("  Description: ").strip()
        amount = ask_float("  Amount (£): ")
        source = input("  Source (e.g. Employment, Freelance): ").strip()
        taxable = ask_choice("  Is this taxable?", ["y", "n"]) == "y"
        add_income(desc, amount, source, is_taxable=taxable)
 
    elif choice == "2":
        # Collect expense details
        desc = input("  Description: ").strip()
        amount = ask_float("  Amount (£): ")
        category = input("  Category (Food/Entertainment/Education/etc.): ").strip()
        importance = ask_choice("  Need or Want?", ["Need", "Want"])
        add_expense(desc, amount, category, importance)
 
    elif choice == "3":
        # Collect recurring bill details
        desc = input("  Description: ").strip()
        amount = ask_float("  Amount (£): ")
        category = input("  Category: ").strip()
        importance = ask_choice("  Need or Want?", ["Need", "Want"])
        freq = ask_choice("  Frequency?", ["monthly", "weekly", "yearly"])
        add_recurring_bill(desc, amount, category, importance, frequency=freq)
 
    elif choice == "0":
        return
    else:
        print("  Invalid option.")
 
 
def menu_remove_transaction():
    """Sub-menu: view all transactions then remove one by ID."""
    view_all_transactions()
    txn_id = input("\n  Enter Transaction ID to remove (e.g. TXN003): ").strip().upper()
    if txn_id:
        # Double-check with the user before deleting
        confirm = ask_choice(f"  Remove {txn_id}? This cannot be undone.", ["y", "n"])
        if confirm == "y":
            remove_transaction(txn_id)
    else:
        print("  No ID entered.")
 
 
def menu_budgets():
    """Sub-menu: budget overview, alerts, and editing."""
    print("\n  Budgets")
    print("  1. View budget summary")
    print("  2. Check alerts")
    print("  3. Update a budget limit")
    print("  0. Back")
 
    choice = input("\n  Choice: ").strip()
 
    if choice == "1":
        view_budget_summary()
    elif choice == "2":
        check_budget_alerts()
    elif choice == "3":
        category = input("  Category name: ").strip()
        amount = ask_float("  New limit (£): ")
        set_budget(category, amount)
    elif choice == "0":
        return
    else:
        print("  Invalid option.")
 
 
def menu_analysis():
    """Sub-menu: various analysis views."""
    print("\n  Analysis")
    print("  1. Needs vs. Wants breakdown")
    print("  2. Spending histogram")
    print("  3. Upcoming bills")
    print("  0. Back")
 
    choice = input("\n  Choice: ").strip()
 
    if choice == "1":
        needs_vs_wants_breakdown()
    elif choice == "2":
        display_spending_histogram()
    elif choice == "3":
        upcoming_bills()
    elif choice == "0":
        return
    else:
        print("  Invalid option.")
 
 
# ─────────────────────────────────────────────
#  DASHBOARD / WELCOME SCREEN
# ─────────────────────────────────────────────
 
def print_dashboard():
    """Show a quick summary at the top of every main menu visit."""
    summary = get_summary()
    print("\n" + "═" * 50)
    print("   💰  FinTrack — Personal Finance CLI")
    print("═" * 50)
    print(f"   Balance:   £{summary['balance']:.2f}")
    print(f"   Income:    £{summary['total_income']:.2f}   Expenses: £{summary['total_expenses']:.2f}")
    net = summary["net"]
    # Use a coloured symbol (green ▲ / red ▼) to hint at positive/negative net
    net_symbol = "▲" if net >= 0 else "▼"
    print(f"   Net:       {net_symbol} £{abs(net):.2f}")
    print("─" * 50)
 
 
# ─────────────────────────────────────────────
#  MAIN MENU LOOP
# ─────────────────────────────────────────────
 
def main():
    """Launch FinTrack and loop until the user chooses to exit."""
    while True:
        print_dashboard()
        print("  1. View Transactions")
        print("  2. Add Transaction")
        print("  3. Remove Transaction")
        print("  4. Budgets")
        print("  5. Analysis")
        print("  0. Exit")
 
        choice = input("\n  Choose an option: ").strip()
 
        if choice == "1":
            menu_view_transactions()
        elif choice == "2":
            menu_add_transaction()
        elif choice == "3":
            menu_remove_transaction()
        elif choice == "4":
            menu_budgets()
        elif choice == "5":
            menu_analysis()
        elif choice == "0":
            print("\n  Goodbye! Stay on budget. 👋\n")
            break
        else:
            print("  Invalid option — please enter a number from the menu.")
 
        # Pause so the user can read output before redrawing the dashboard
        input("\n  Press Enter to continue...")
 
 
# Standard Python entry-point guard
if __name__ == "__main__":
    main()