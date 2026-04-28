from transaction import Transaction


#adding category and importance on top of the base feilds
class Expense(Transaction):
    def init(self, amount, description, category, importance, date=None):
        super().init(amount, description, date) #let the parent class handle amouint, description and date
        self.category = category #example "food"
        self.importance = importance #example "essential"

    def get_category(self):
        return self.category

    def get_importance(self):
        return self.importance

    def set_category(self, category):
        self.category = category

    def set_importance(self, importance):
        self.importance = importance

    def display_details(self):
        #call the parent's display first then tack on the expenses fields
        return (f"{super().display_details()} | "
                f"Category: {self.category} | Importance: {self.importance} | Type: Expense")

    def to_dict(self):
        data = super().to_dict() #start with whatever the parent serialises (amount, description)
        data["type"] = "expense"
        data["category"] = self.category
        data["importance"] = self.importance
        return data