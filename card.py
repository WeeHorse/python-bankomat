import re

from pydantic import BaseModel, field_validator

from account import Account


class Card(BaseModel):
    pin: str = ""
    account: Account
    valid: bool = True

    class Config:
        validate_default = True

    @classmethod
    def create(cls, account: Account) -> "Card":
        return cls(account=account)

    @field_validator('pin')
    @classmethod
    def pin_must_be_valid(cls, pin: str) -> str:
        pattern = r'^$|^\d{4}$'
        if not re.match(pattern, pin):
            raise ValueError("PIN must me empty string or 4 numbers in the format XXXX")
        return pin

    def invalidate(self):
        self.valid = False

    def set_pin(self, pin):
        # explicit call to validator
        self.pin_must_be_valid(pin)
        # we could skip "our own" validation now..
        if(self.pin == "" and len(pin) == 4): # will pass any string of length 4
            self.pin = pin
            return True
        else:
            return False


