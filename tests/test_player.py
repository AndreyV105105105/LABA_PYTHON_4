import pytest
from src.entities.player import Player


def test_player_initial_balance_non_negative():
    p = Player("A", -100)
    assert p.balance == 0
    assert p.is_bankrupt is True


def test_player_make_bet_validation():
    p = Player("A", 100)
    with pytest.raises(ValueError):
        p.make_bet(0)
    with pytest.raises(ValueError):
        p.make_bet(-1)


def test_player_make_bet_insufficient_funds():
    p = Player("A", 50)
    assert p.make_bet(100) is False
    assert p.balance == 50


def test_player_receive_cash_validation():
    p = Player("A", 100)
    with pytest.raises(ValueError):
        p.receive_cash(0)
    with pytest.raises(ValueError):
        p.receive_cash(-10)


def test_player_bankruptcy_flag_updates():
    p = Player("A", 10)
    assert p.make_bet(10) is True
    assert p.balance == 0
    assert p.is_bankrupt is True

    p.receive_cash(5)
    assert p.balance == 5
    assert p.is_bankrupt is False

    p.go_bankrupt()
    assert p.balance == 0
    assert p.is_bankrupt is True
