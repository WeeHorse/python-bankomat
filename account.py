import random


class Account:
    def __init__(self, first_name, last_name, ssn):
        self.balance = 0
        self.first_name = first_name
        self.last_name = last_name
        self.ssn = ssn
        self.account_nr = self.generateAccountNr()

    def generateAccountNr(self):
        return "".join(random.choices('0123456789', k=10))

    def get_account_nr(self):
        return self.account_nr

    def withdraw(self, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            return amount
        else:
            return 0

    def deposit(self, amount):
        self.balance += amount
        return amount

    def get_balance(self):
        return self.balance