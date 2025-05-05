from bankomat import Bankomat
from account import Account
from card import Card

def main():
    bankomat = Bankomat()
    bankomat.add_cash(100,50)
    bankomat.add_cash(200, 20)
    bankomat.add_cash(500, 4)
    account = Account.create("Benjamin", "Berglund", "19700109-2456")
    account.deposit(6000)
    card = Card(account)

    bankomat.insert_card(card)
    print(bankomat.get_message())

    bankomat.init_card("012")
    print(bankomat.get_message())

    bankomat.init_card("0123")
    print(bankomat.get_message())

    bankomat.enter_pin("1234")
    print(bankomat.get_message())

    bankomat.enter_pin("0123")
    print(bankomat.get_message())

    bankomat.withdraw(15000)
    print(bankomat.get_message())

    bankomat.withdraw(8000)
    print(bankomat.get_message())

    bankomat.withdraw(3000)
    print(bankomat.get_message())

    bankomat.eject_card()
    print(bankomat.get_message())

    bankomat.withdraw(100)
    print(bankomat.get_message())

    bankomat.insert_card(card)
    print(bankomat.get_message())

    bankomat.enter_pin("0123")
    print(bankomat.get_message())

    bankomat.withdraw(1000)
    print(bankomat.get_message())

    print(bankomat.machine_balance())

    bankomat.eject_card()
    print(bankomat.get_message())

if __name__ == "__main__":
    main()

