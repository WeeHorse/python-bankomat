import pytest
from bankomat import Bankomat
from account import Account
from card import Card

def test_insert_card():
    bankomat = Bankomat()
    account = Account.create("Benjamin", "Berglund", "700109-2456")
    card = Card(account)
    result = bankomat.insert_card(card)
    assert result == True

def test_eject_card():
    bankomat = Bankomat()
    account = Account.create("Benjamin", "Berglund", "700109-2456")
    card = Card(account)
    bankomat.insert_card(card)
    result = bankomat.eject_card()
    assert result == None

def test_init_card():
    bankomat = Bankomat()
    account = Account.create("Benjamin", "Berglund", "700109-2456")
    card = Card(account)
    bankomat.insert_card(card)
    result = bankomat.init_card("0123")
    assert result == True

def test_enter_invalid_pin():
    bankomat = Bankomat()
    account = Account.create("Benjamin", "Berglund", "700109-2456")
    card = Card(account)
    bankomat.insert_card(card)
    bankomat.init_card("0123")
    result = bankomat.enter_pin("1234")
    assert result == False


def test_enter_valid_pin():
    bankomat = Bankomat()
    account = Account.create("Benjamin", "Berglund", "700109-2456")
    card = Card(account)
    bankomat.insert_card(card)
    bankomat.init_card("0123")
    result = bankomat.enter_pin("0123")
    assert result == True

# Fixture (helper method to avoid all this repetitive code)
@pytest.fixture
def banko():
    bankomat = Bankomat()
    bankomat.add_cash(100,50)
    bankomat.add_cash(200, 20)
    bankomat.add_cash(500, 4)
    account = Account.create("Benjamin", "Berglund", "700109-2456")
    account.deposit(6000)
    card = Card(account)
    bankomat.insert_card(card)
    bankomat.init_card("0123")
    bankomat.enter_pin("0123")
    return bankomat

def test_withdraw_1000(banko):
    # setup
    withdrawal = 1000
    initial_machine_balance = banko.machine_balance()
    account = banko.card.account
    initial_account_balance = account.get_balance()
    # test
    result = banko.withdraw(withdrawal)
    assert result == withdrawal
    assert initial_account_balance == account.get_balance() + withdrawal
    assert banko.machine_balance() + result == initial_machine_balance

def test_withdraw_all(banko):
    result = banko.withdraw(6000)
    assert result == 6000
    assert banko.card.account.get_balance() == 0

def test_withdraw_half(banko):
    result = banko.withdraw(3000)
    assert result == 3000
    assert banko.card.account.get_balance() == 3000

def test_overdraw_account(banko):
    result = banko.withdraw(7000)
    assert result == 0
    assert banko.card.account.get_balance() == 6000

def test_overdraw_bankomat(banko):
    # setup (increase account to 12000)
    banko.card.account.deposit(6000)
    # test
    result = banko.withdraw(12000)
    assert result == 0
    assert banko.machine_balance() == 11000
    assert banko.card.account.get_balance() == 12000
