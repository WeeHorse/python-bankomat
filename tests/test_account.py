import pytest
from account import Account
from pydantic import ValidationError

def test_account_creation_ssn_10():
    account = Account.create("Benjamin", "Berglund", "750109-2456")
    assert len(account.ssn) == 11
    assert len(account.get_account_nr()) == 10

def test_account_creation_ssn_12():
    account = Account.create("Benjamin", "Berglund", "19750109-2456")
    assert len(account.ssn) == 13
    assert len(account.get_account_nr()) == 10

def test_fail_account_creation_ssn_11():
    with pytest.raises(ValidationError) as exc_info:
        Account.create("Benjamin", "Berglund", "9700109-2456")
    assert "SSN must me 10 or 12 numbers in the format YYMMDD-XXXX or YYYYMMDD-XXXX" in str(exc_info.value)

def test_deposit_1000():
    account = Account.create("Benjamin", "Berglund", "700109-2456")
    account.deposit(1000)
    assert account.get_balance() == 1000

def test_deposit_negative():
    account = Account.create("Benjamin", "Berglund", "700109-2456")
    with pytest.raises(ValueError) as exc_info:
        account.deposit(-1000)
    assert "Balance cannot be negative" in str(exc_info.value)