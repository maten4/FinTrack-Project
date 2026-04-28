from transaction import Transaction

class RecurringBill(Transaction):
    def __init__(self, amount, description, category, importance, frequency, next_due_date, date=None):
        super().__init__(amount, description, date) # let the parent handle amount, description and date
        self.__category = category #eg utilities
        self.__importance = importance #eseential or optional
        self.__frequency = frequency  # "monthly", "weekly"
        self.__next_due_date = next_due_date  # "YYYY-MM-DD" the forecast uses this to know when to deduct it

    def get_category(self):
        return self.__category

    def get_importance(self):
        return self.__importance

    def get_frequency(self):
        return self.__frequency

    def get_next_due_date(self):
        return self.__next_due_date

    def set_next_due_date(self, date):
        self.__next_due_date = date #needs updating after each occurance so it stays accurate

    def display_details(self):
        #call the parent's dispaly first 
        return (f"{super().display_details()} | "
                f"Category: {self.__category} | Importance: {self.__importance} | "
                f"Frequency: {self.__frequency} | Next Due: {self.__next_due_date} | Type: RecurringBill")

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "recurring_bill"
        data["category"] = self.__category
        data["importance"] = self.__importance
        data["frequency"] = self.__frequency
        data["next_due_date"] = self.__next_due_date
        return data