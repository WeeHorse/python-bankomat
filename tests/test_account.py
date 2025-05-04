import pytest
from account import Account
from pydantic import ValidationError

def test_account_creation_ssn_10():
    account = Account.create("Benjamin", "Berglund", "700109-2456")
    assert len(account.ssn) == 11
    assert len(account.get_account_nr()) == 10

def test_account_creation_ssn_12():
    account = Account.create("Benjamin", "Berglund", "19700109-2456")
    assert len(account.ssn) == 13
    assert len(account.get_account_nr()) == 10

def test_fail_account_creation_ssn_11():
    with pytest.raises(ValidationError) as exc_info:
        Account.create("Benjamin", "Berglund", "9700109-2456")
    assert "SSN must be 10 or 12 numbers" in str(exc_info.value)

def test_deposit_1000():
    account = Account.create("Benjamin", "Berglund", "700109-2456")
    account.deposit(1000)
    assert account.get_balance() == 1000

