import pytest
from bankomat import Bankomat
from account import Account
from card import Card

def test_insert_card():
    bankomat = Bankomat()
    account = Account("Benjamin", "Berglund", "700109-2456")
    card = Card(account)
    result = bankomat.insert_card(card)
    assert isinstance(result, Card)

def test_eject_card():
    bankomat = Bankomat()
    account = Account("Benjamin", "Berglund", "700109-2456")
    card = Card(account)
    bankomat.insert_card(card)
    bankomat.eject_card()
    assert not isinstance(bankomat.card, Card)