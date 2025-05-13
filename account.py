from pydantic import BaseModel, Field, field_validator
import random
import re               # re = regex

def generate_account_nr() -> str:
    return ''.join(random.choices('0123456789', k=10))

class Account(BaseModel):
    balance: int = 0
    first_name: str
    last_name: str
    ssn: str
    account_nr: str = generate_account_nr()

    class Config:
        validate_default = True

    @classmethod
    def create(cls, first_name: str, last_name: str, ssn: str) -> "Account":
        return cls(first_name=first_name, last_name=last_name, ssn=ssn)

    @field_validator('ssn')
    @classmethod
    def ssn_must_be_valid(cls, ssn: str) -> str:
        pattern = r'^(?:\d{6}|\d{8})-\d{4}$'
        if not re.match(pattern, ssn):
            raise ValueError("SSN must me 10 or 12 numbers in the format YYMMDD-XXXX or YYYYMMDD-XXXX")
        return ssn

    @field_validator('balance')
    @classmethod
    def balance_must_be_non_negative(cls, balance: int) -> int:
        if balance < 0:
            raise ValueError("Balance cannot be negative")
        return balance

    def withdraw(self, amount: int) -> int:
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            return amount
        return 0

    def deposit(self, amount: int) -> int:
        # alternatively we could just have used a regular if case to prevent a negative deposit,
        # which we really should do, but let's just use the validator anyway, so that it can error:)
        self.balance += amount
        # instead we use validator (after instanciation, like now, when calling a method)
        self.balance_must_be_non_negative(self.balance)
        return amount

    def get_balance(self) -> int:
        return self.balance

    def get_account_nr(self) -> str:
        return self.account_nr

