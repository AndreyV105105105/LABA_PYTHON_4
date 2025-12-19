import pytest
from src.entities.chip import Chip


def test_chip_standard_nominal_and_total():
    c = Chip("красная", 2)
    assert c.color == "красная"
    assert c.value == 5
    assert c.amount == 2
    assert c.total == 10


def test_chip_invalid_color_raises():
    with pytest.raises(ValueError):
        Chip("гусиная", 1)


def test_chip_add_same_color():
    a = Chip("синяя", 3)
    b = Chip("синяя", 2)
    c = a + b
    assert c.color == "синяя"
    assert c.value == 10
    assert c.amount == 5


def test_chip_add_different_color_raises():
    a = Chip("синяя", 1)
    b = Chip("красная", 1)
    with pytest.raises(ValueError):
        er = a + b


def test_chip_split_ok():
    c = Chip("зелёная", 5)
    taken, rem = c.split(2)
    assert taken.amount == 2
    assert taken.total == 50
    assert rem is not None
    assert rem.amount == 3


def test_chip_split_errors():
    c = Chip("белая", 2)
    with pytest.raises(ValueError):
        c.split(0)
    with pytest.raises(ValueError):
        c.split(3)
