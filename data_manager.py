import json
import os

DATA_FILE = "./data/transactions.json" #path to where data is on the disk

def load_data():
    #if it doesnt exist yet, just return empty default values
    if not os.path.exists(DATA_FILE):
        return {"current_balance": 0.0, "transactions": [], "budgets": {}}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f) #reads the file and converts the JSON into python
    except (json.JSONDecodeError, IOError):
        #file exists but is corrupted or unreadable
        print("Warning: Data file corrupted, starting fresh.")
        return {"current_balance": 0.0, "transactions": [], "budgets": {}}

def save_data(data):
    os.makedirs("./data", exist_ok=True) #create data folder if it doesmt exist yet
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4) #converts the dictionaty back into JSON
        print("Data saved successfully.")
    except IOError:
        print("Error: Could not save data.") #debug message if something went wrong