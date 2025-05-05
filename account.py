from pydantic import BaseModel, Field, field_validator
from psycopg2.extensions import connection as PgConnection
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
    conn: PgConnection
    model_config = {
        "arbitrary_types_allowed": True
    }

    @classmethod
    def create(cls, first_name: str, last_name: str, ssn: str, conn) -> "Account":
        account = cls(first_name=first_name, last_name=last_name, ssn=ssn, conn=conn)
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO accounts (first_name, last_name, ssn, balance, account_nr) VALUES (%s, %s, %s, %s, %s)",
                (account.first_name, account.last_name, account.ssn, account.balance, account.account_nr)
            )
            conn.commit()
        return account

    @classmethod
    def load_by_account_nr(cls, account_nr: str) -> "Account":
        with cls.conn.cursor() as cur:
            cur.execute("SELECT first_name, last_name, ssn, balance, account_nr FROM accounts WHERE account_nr = %s", (account_nr,))
            row = cur.fetchone()
            if row:
                return cls(first_name=row[0], last_name=row[1], ssn=row[2], balance=row[3], account_nr=row[4])
            raise ValueError("Account not found")

    def save(self):
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE accounts SET balance = %s WHERE account_nr = %s",
                (self.balance, self.account_nr)
            )
            self.conn.commit()

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
            self.save()
            return amount
        return 0

    def deposit(self, amount: int) -> int:
        if amount > 0:
            self.balance += amount
            self.save()
            return amount
        return 0

    def get_balance(self) -> int:
        return self.balance

    def get_account_nr(self) -> str:
        return self.account_nr