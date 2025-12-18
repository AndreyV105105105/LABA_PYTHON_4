from __future__ import annotations


class Chip:
    """
    Фишка казино (пачка фишек одного цвета).

    color берётся только из STANDARD_CHIPS, value вычисляется автоматически.
    __add__ объединяет пачки фишек одинакового цвета (и, соответственно, номинала).
    """
    # Стандартные цвета и номиналы фишек казино
    STANDARD_CHIPS = {
        "белая": 1,
        "красная": 5,
        "синяя": 10,
        "зелёная": 25,
        "чёрная": 100,
        "фиолетовая": 500,
        "оранжевая": 1000,
        "розовая": 5000,
    }

    def __init__(self, color: str, amount: int = 1):
        if not isinstance(color, str) or not color.strip():
            raise ValueError("Цвет фишки должен быть непустой строкой")

        color = color.strip().lower()

        if color not in self.STANDARD_CHIPS:
            raise ValueError(
                f"Неизвестный цвет фишки: {color!r}. Допустимые: {', '.join(self.STANDARD_CHIPS.keys())}"
            )

        if not isinstance(amount, int):
            raise TypeError("Количество фишек должно быть int")
        if amount <= 0:
            raise ValueError("Количество фишек должно быть больше 0")

        self._color = color
        self._value = self.STANDARD_CHIPS[color]
        self._amount = amount

    @property
    def color(self) -> str:
        return self._color

    @property
    def value(self) -> int:
        return self._value

    @property
    def amount(self) -> int:
        return self._amount

    @property
    def total(self) -> int:
        """Суммарная стоимость пачки фишек."""
        return self._value * self._amount

    def split(self, amount_take: int) -> tuple["Chip", "Chip | None"]:
        """
        Отделить `take` фишек от пачки.

        Возвращает:
          (взятая пачка, остаток или None)
        """
        if not isinstance(amount_take, int):
            raise TypeError("amount_take должен быть int")
        if amount_take <= 0:
            raise ValueError("amount_take должен быть больше 0")
        if amount_take > self._amount:
            raise ValueError("Нельзя отделить больше фишек, чем есть в пачке")

        taken = Chip(self._color, amount_take)
        rest = self._amount - amount_take
        remainder = Chip(self._color, rest) if rest > 0 else None
        return taken, remainder

    def __add__(self, other: "Chip") -> "Chip":
        """
        Объединение пачек фишек одного цвета.
        """
        if not isinstance(other, Chip):
            return NotImplemented

        if self._color != other.color:
            raise ValueError(
                f"Нельзя складывать фишки разных цветов: {self._color!r} и {other.color!r}"
            )

        # номинал гарантированно совпадает, т.к. определяется по цвету
        return Chip(self._color, self._amount + other.amount)

    def __str__(self) -> str:
        return f"Фишки: {self._color} (номинал {self._value}) x{self._amount} = {self.total}"

    def __repr__(self) -> str:
        return f"Chip(color='{self._color}', amount={self._amount})"
