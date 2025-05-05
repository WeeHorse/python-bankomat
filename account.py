from pydantic import BaseModel, Field, field_validator
import random
import re

def generate_account_nr() -> str:
    return ''.join(random.choices('0123456789', k=10))

class Account(BaseModel):
    first_name: str
    last_name: str
    ssn: str
    balance: int = 0
    account_nr: str = Field(default_factory=generate_account_nr)

    @classmethod
    def create(cls, first_name: str, last_name: str, ssn: str) -> "Account":
        # add validation logic... or use @field validator methods
        return cls(first_name=first_name, last_name=last_name, ssn=ssn)

    @field_validator('balance')
    @classmethod
    def balance_must_be_non_negative(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Balance cannot be negative")
        return v

    @field_validator('ssn')
    @classmethod
    def ssn_format_must_be_valid(cls, v: str) -> str:
        pattern = r'^(?:\d{6}|\d{8})-\d{4}$'
        if not re.match(pattern, v):
            raise ValueError("SSN must be 10 or 12 numbers in the format YYMMDD-XXXX or YYYYMMDD-XXXX")
        return v

    def withdraw(self, amount: int) -> int:
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            return amount
        return 0

    def deposit(self, amount: int) -> int:
        if amount > 0:
            self.balance += amount
            return amount
        return 0

    def get_balance(self) -> int:
        return self.balance

    def get_account_nr(self) -> str:
        return self.account_nr
