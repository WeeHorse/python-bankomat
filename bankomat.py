from card import Card


class Bankomat:
    def __init__(self):
        self.card_inserted = False
        self.card = None
        self.valid_card = False
        self.msgs = []
        self._cash = {
            100:0,
            200:0,
            500:0
        }

    def machine_balance(self):
        return sum(bill * count for bill, count in self._cash.items())

    def add_cash(self, bill, amount):
        self._cash[bill] = self._cash[bill] + amount

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
        self.valid_card = False
        self.msgs.append("Card removed, don't forget it!")
        return self.card

    def init_card(self, pin):
        result = self.card.set_pin(pin)
        if result == True:
            self.msgs.append("Pin set successfully!")
        else:
            self.msgs.append("The pin you entered is invalid!")
        return result

    def enter_pin(self, pin):
        if(self.card == None):
            self.msgs.append("no card inserted")
            return None
        elif self.card.pin == pin:
            self.msgs.append("Correct pin")
            self.valid_card = True
            return self.valid_card
        else:
            self.msgs.append("Incorrect pin")
            self.valid_card = False
            return self.valid_card

    def try_withdraw_bills(self, amount):
        result = {}
        remaining = amount

        # Create a temporary copy so we don't change original state unless successful
        temp_money = self._cash.copy()

        for bill in sorted(temp_money.keys(), reverse=True):
            max_needed = remaining // bill
            num_to_use = min(max_needed, temp_money[bill])
            if num_to_use > 0:
                result[bill] = num_to_use
                remaining -= bill * num_to_use
                temp_money[bill] -= num_to_use

        if remaining == 0:
            # Commit the withdrawal to the real money inventory
            for bill, count in result.items():
                self._cash[bill] -= count
            return result
        else:
            return None

    def withdraw(self, amount):
        if (self.card == None):
            self.msgs.append("No card inserted")
            return None
        elif (self.valid_card == False):
            self.msgs.append("Your card is invalid")
            return None
        # Note that bills are withdrawn from the machine in the last case in the elif condition, if successful
        elif amount > 0 and amount <= self.machine_balance() and amount <= self.card.account.get_balance() and self.try_withdraw_bills(amount):
            self.card.account.withdraw(amount)
            self.msgs.append(f"Withdrawing {amount}")
            return amount
        else:
            if amount > self.machine_balance():
                self.msgs.append("Machine has insufficient funds")
            elif amount > self.card.account.get_balance():
                self.msgs.append("Card has insufficient funds")
            else:
                self.msgs.append("You cannot withdraw 0 or less money")
            return 0
