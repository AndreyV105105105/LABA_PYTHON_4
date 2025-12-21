# import pytest
from src.custom_collections.player_collection import PlayerCollection
from src.entities.player import Player

def test_player_collection_getitem_index(capsys):
    pc = PlayerCollection()
    pc.add_player(Player("A", 100))
    pc.add_player(Player("B", 200))
    capsys.readouterr()

    p0 = pc[0]
    assert p0.name in {"A", "B"}  # порядок зависит от порядка регистрации в CasinoBalance


def test_player_collection_remove_and_find(capsys):
    pc = PlayerCollection()
    pc.add_player(Player("A", 100))
    pc.add_player(Player("B", 200))
    capsys.readouterr()

    assert pc.find_player("A") is not None
    removed = pc.remove_player("A")
    assert removed is not None
    assert pc.find_player("A") is None


def test_player_collection_slice_behavior_expected(capsys):
    pc = PlayerCollection()
    pc.add_player(Player("A", 100))
    pc.add_player(Player("B", 200))
    pc.add_player(Player("C", 300))
    capsys.readouterr()

    part = pc[0:2]
    assert len(part) == 2
    names = [p.name for p in part]
    assert len(names) == 2
