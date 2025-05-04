import pytest
from account import Account

def test_account_creation():
    account = Account("Benjamin", "Berglund", "700109-2456")
    assert len(account.ssn) == 11 or len(account.ssn) == 13

def test_deposit_1000():
    account = Account("Benjamin", "Berglund", "700109-2456")
    account.deposit(1000)
    assert account.get_balance() == 1000

