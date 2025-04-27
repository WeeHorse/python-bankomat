class Account:
    def __init__(self):
        self.balance = 5000

    def withdraw(self, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            return amount
        else:
            return 0

    def get_balance(self):
        return self.balance