import pytest
from account import Account

def test_account_creation():
    account = Account("Benjamin", "Berglund", "700109-2456")
    assert len(account.ssn) == 11 or len(account.ssn) == 13
