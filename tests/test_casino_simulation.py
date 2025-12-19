from src.entities.casino import Casino
from src.entities.player import Player
from src.entities.goose import Goose, WarGoose, HonkGoose


def _make_casino() -> Casino:
    c = Casino()
    c.register_player(Player("A", 500))
    c.register_player(Player("B", 500))

    c.register_goose(Goose("G1", honk_volume=1))
    c.register_goose(WarGoose("G2", honk_volume=5))
    c.register_goose(HonkGoose("G3", honk_volume=10))
    return c


def test_run_simulation_reproducible_with_seed(capsys):
    c1 = _make_casino()
    c1.run_simulation(steps=3, seed=123)
    out1 = capsys.readouterr().out

    c2 = _make_casino()
    c2.run_simulation(steps=3, seed=123)
    out2 = capsys.readouterr().out

    assert out1 == out2
