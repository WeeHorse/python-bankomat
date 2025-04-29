from card import Card


class Bankomat:
    def __init__(self):
        self.card_inserted = False
        self.card = None
        self.machine_balance = 11000
        self.msgs = []

    def get_message(self):
        msg = ""
        if self.msgs:
            msg = self.msgs.pop(0)
        return msg

    def insert_card(self, card):
        self.card_inserted = True
        self.card = card
        self.msgs.append("Card inserted. Enter pin.")
        return self.card_inserted

    def eject_card(self):
        self.card_inserted = False
        self.card = None
        self.msgs.append("Card removed, don't forget it!")
        return self.card

    def enter_pin(self, pin):
        if(self.card == None):
            self.msgs.append("no card inserted")
            return None
        elif self.card.pin == pin:
            self.msgs.append("Correct pin")
            return True
        else:
            self.msgs.append("Incorrect pin")
            return False

    def withdraw(self, amount):
        if (self.card == None):
            self.msgs.append("no card inserted")
            return None
        elif amount > 0 and amount <= self.machine_balance and amount <= self.card.account.get_balance():
            self.machine_balance -= amount
            self.card.account.withdraw(amount)
            self.msgs.append(f"Withdrawing {amount}")
            return amount
        else:
            if amount > self.machine_balance:
                self.msgs.append("Machine has insufficient funds")
            elif amount > self.card.account.get_balance():
                self.msgs.append("Card has insufficient funds")
            else:
                self.msgs.append("You cannot withdraw 0 or less money")
            return 0
