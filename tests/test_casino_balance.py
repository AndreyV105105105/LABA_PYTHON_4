# import pytest
from src.custom_collections.casinoBalance import CasinoBalance
from src.entities.player import Player


def test_casino_balance_register_and_getitem(capsys):
    cb = CasinoBalance()
    p = Player("A", 100)

    cb.register_player(p)
    capsys.readouterr()  # гасим лог

    assert cb["A"] == 100


def test_casino_balance_setitem_logs(capsys):
    cb = CasinoBalance()
    cb.register_player(Player("A", 100))
    capsys.readouterr()

    cb["A"] = 12
    out = capsys.readouterr().out
    assert "A" in out  # проверяем, что лог реально печатается

    assert cb["A"] == 12
    log = cb.get_transaction_log("A")
    assert len(log) >= 2  # регистрация + изменение
    assert log[-1]["new_balance"] == 12


def test_casino_balance_make_bet_and_receive_cash(capsys):
    cb = CasinoBalance()
    cb.register_player(Player("A", 100))
    capsys.readouterr()

    assert cb.make_bet("A", 10) is True
    assert cb["A"] == 90

    assert cb.receive_cash("A", 20) is True
    assert cb["A"] == 110


def test_casino_balance_make_bet_invalid_player():
    cb = CasinoBalance()
    assert cb.make_bet("vever", 10) is False
    assert cb.receive_cash("vever", 10) is False

