from datetime import datetime, timedelta

def forecast_balance(data):
    balance = data["current_balance"]
    today = datetime.today()
    forecast = []

    #get recurring bills 
    recurring = [t for t in data["transactions"] if t["type"] == "recurring_bill"]

    #loop through each of the next 30 days
    for day_offset in range(1, 31):
        current_day = today + timedelta(days=day_offset)
        current_day_str = current_day.strftime("%Y-%m-%d") #converts to string
        daily_change = 0
        
        #using a for loop it checks if any bills are due today
        for bill in recurring:
            if bill["next_due_date"] == current_day_str:
                daily_change -= bill["amount"] #subtract it from the balance
        
        #apply whatever changed today to the running balance
        balance += daily_change
        forecast.append({
            "date": current_day_str,
            "balance": round(balance, 2), #round to 2 decimals so it's correct for money
            "change": round(daily_change, 2)
        })

    return forecast

def print_forecast(data):
    forecast = forecast_balance(data)
    print("\n--- 30 Day Forecast ---")
    for entry in forecast:
        #only prints days where something actually happend
        if entry["change"] != 0:
            print(f"{entry['date']} | Balance: £{entry['balance']:.2f} | Change: £{entry['change']:.2f}")
            #grab the last entry in the list to show the final balance after all days
    print(f"\nFinal balance in 30 days: £{forecast[-1]['balance']:.2f}")