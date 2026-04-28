import uuid
from datetime import datetime

#base class for all transactions
class Transaction:
    def init(self, amount, description, date=None): 
        self.id = str(uuid.uuid4())[:8].upper() #generate a random id and take the first 8 characters
        self.date = date if date else datetime.today().strftime("%Y-%m-%d") #use provided date or default to today
        self.amount = amount
        self.description = description

    def get_id(self):
        return self.id

    def get_date(self):
        return self.date

    def get_amount(self):
        return self.amount

    def get_description(self):
        return self.description

    # Setters
    def set_amount(self, amount):
        self.amount = amount

    def set_description(self, description):
        self.description = description


    def display_details(self):
        # base display that subclasses call via super() then append their own fields
        return (f"ID: {self.id} | Date: {self.date} | "
                f"Amount: £{self.amount:.2f} | Desc: {self.description}")

    def to_dict(self):
        #serialise to a plain dict so it can be saved to JSON
        return {
            "id": self.id,
            "date": self.date,
            "amount": self.amount,
            "description": self.description
        }