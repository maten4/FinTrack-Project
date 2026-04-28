from transaction import Transaction

#income extends transaction 
class Income(Transaction):
    def __init__(self, amount, description, source, is_taxable, date=None):
        super().__init__(amount, description, date) #let the parent handle the amount , description and date
        self.__source = source # example: salary
        self.__is_taxable = is_taxable #bool matters for tax calcualtion later

    def get_source(self):
        return self.__source
    
    def get_is_taxable(self):
        return self.__is_taxable
    
    def set_source(self,source):
        self.__source = source

    def display_details(self):
        taxable = "Yes" if self.__is_taxable else "No" #converts the bool to something readable
        return (f"{super().display_details()} "
                f"Sorce: {self.__source} Taxable: {taxable} Type: Income")
    
    def to_dict(self):
        data = super().to_dict() #start with whatever the parent serialises
        data["type"] = "income" #tag it so we know what class to reconstruct
        data["source"] = self.__source
        data["is_taxable"] = self.__is_taxable
        return data