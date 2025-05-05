import pytest
from account import Account
from pydantic import ValidationError
from db_model import DBModel
db = DBModel.from_dsn("dbname=bankomat user=postgres password=root host=localhost port=5432")
conn = db.get_connection()

def test_account_creation_ssn_10():
    account = Account.create("Benjamin", "Berglund", "700109-2456", conn)
    assert len(account.ssn) == 11
    assert len(account.get_account_nr()) == 10

def test_account_creation_ssn_12():
    account = Account.create("Bill", "Berglund", "19700109-2456", conn)
    assert len(account.ssn) == 13
    assert len(account.get_account_nr()) == 10

def test_fail_account_creation_ssn_11():
    with pytest.raises(ValidationError) as exc_info:
        Account.create("Beo", "Berglund", "9700109-2456", conn)
    assert "SSN must be 10 or 12 numbers" in str(exc_info.value)

def test_deposit_1000():
    account = Account.create("Bob", "Berglund", "710109-2456", conn)
    account.deposit(1000)
    assert account.get_balance() == 1000

