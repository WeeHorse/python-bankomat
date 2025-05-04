class Card:

    def __init__(self, account):
        self.pin = ""
        self.account = account
        self.valid = True

    def invalidate(self):
        self.valid = False

    def set_pin(self, pin):
        if(self.pin == "" and len(pin) == 4):
            self.pin = pin
            return True
        else:
            return False


