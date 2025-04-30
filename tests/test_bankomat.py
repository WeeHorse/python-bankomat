import pytest
from bankomat import Bankomat
from account import Account
from card import Card

def test_insert_card():
    bankomat = Bankomat()
    account = Account("Benjamin", "Berglund", "700109-2456")
    card = Card(account)
    result = bankomat.insert_card(card)
    assert result == True

def test_eject_card():
    bankomat = Bankomat()
    account = Account("Benjamin", "Berglund", "700109-2456")
    card = Card(account)
    bankomat.insert_card(card)
    result = bankomat.eject_card()
    assert result == None

def test_enter_invalid_pin():
    bankomat = Bankomat()
    account = Account("Benjamin", "Berglund", "700109-2456")
    card = Card(account)
    bankomat.insert_card(card)
    result = bankomat.enter_pin("1234")
    assert result == False


def test_enter_valid_pin():
    bankomat = Bankomat()
    account = Account("Benjamin", "Berglund", "700109-2456")
    card = Card(account)
    bankomat.insert_card(card)
    result = bankomat.enter_pin("0123")
    assert result == True

def test_withdraw_1000():
    # testdata
    initial_machine_balance = 11000
    initial_account_balance = 1000
    withdrawal = 1000
    # setup
    bankomat = Bankomat()
    bankomat.machine_balance = initial_machine_balance
    account = Account("Benjamin", "Berglund", "700109-2456", initial_account_balance)
    card = Card(account)
    bankomat.insert_card(card)
    bankomat.enter_pin("0123")
    # test
    result = bankomat.withdraw(withdrawal)
    assert result == withdrawal
    assert account.balance == initial_account_balance - withdrawal
    assert bankomat.machine_balance + result == initial_machine_balance


# Example using a  fixture (helper method to avoid all this repetitive code)
@pytest.fixture
def banko():
    bankomat = Bankomat()
    account = Account("Benjamin", "Berglund", "700109-2456", 6000)
    card = Card(account)
    bankomat.insert_card(card)
    bankomat.enter_pin("0123")
    return bankomat

def test_withdraw_all(banko):
    result = banko.withdraw(6000)
    assert result == 6000
    assert banko.card.account.balance == 0

def test_withdraw_half(banko):
    result = banko.withdraw(3000)
    assert result == 3000
    assert banko.card.account.balance == 3000

def test_overdraw_account(banko):
    result = banko.withdraw(7000)
    assert result == 0
    assert banko.card.account.balance == 6000

def test_overdraw_bankomat(banko):
    # special, set lower amount left in machine
    banko.machine_balance = 5000
    result = banko.withdraw(6000)
    assert result == 0
    assert banko.machine_balance == 5000
    assert banko.card.account.balance == 6000
