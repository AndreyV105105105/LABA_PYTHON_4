from __future__ import annotations

from src.custom_collections.casinoBalance import CasinoBalance
from src.entities.player import Player


class PlayerCollection:
    """Списковая коллекция, использует CasinoBalance внутри"""

    def __init__(self, casino_balance: CasinoBalance | None = None):
        if casino_balance is None:
            self._casino_balance = CasinoBalance()
        else:
            self._casino_balance = casino_balance

        # Для быстрого доступа по индексу / срезам
        self._player_names: list[str] = []

        # Если True — это "view" (срез), и индекс НЕ должен перезаписываться полным списком
        self._is_view: bool = False

    @property
    def casino_balance(self) -> CasinoBalance:
        return self._casino_balance

    def _update_index(self) -> None:
        """Обновить индекс имён для быстрого доступа (только для основной коллекции)."""
        if self._is_view:
            return
        self._player_names = list(self._casino_balance.keys())

    def __getitem__(self, key: int | slice) -> Player | PlayerCollection:
        """Доступ по индексу или срезу."""
        self._update_index()

        if isinstance(key, slice):
            new_collection = PlayerCollection(self._casino_balance)
            new_collection._player_names = self._player_names[key]
            new_collection._is_view = True
            return new_collection

        if isinstance(key, int):
            player_name = self._player_names[key]
            return self._casino_balance.get_player(player_name)

        raise TypeError(f"Индекс должен быть int или slice, а не {type(key).__name__}")

    def __len__(self) -> int:
        """Количество игроков (в view = длина среза)."""
        self._update_index()
        return len(self._player_names)

    def __iter__(self):
        """Итерация по игрокам (в view = только игроки среза)."""
        self._update_index()
        for name in self._player_names:
            player = self._casino_balance.get_player(name)
            if player is not None:
                yield player

    def __contains__(self, item: Player | str) -> bool:
        """Проверка наличия игрока."""
        if isinstance(item, Player):
            return item.name in self._casino_balance
        if isinstance(item, str):
            return item in self._casino_balance
        return False

    def add_player(self, player: Player) -> None:
        """Добавить игрока."""
        self._casino_balance.register_player(player)
        if not self._is_view:
            self._update_index()

    def remove_player(self, identifier: Player | str) -> Player | None:
        """Удалить игрока."""
        if isinstance(identifier, Player):
            player_name = identifier.name
        elif isinstance(identifier, str):
            player_name = identifier
        else:
            return None

        player = self._casino_balance.remove_player(player_name)
        if player and not self._is_view:
            self._update_index()
        return player

    def find_player(self, name: str) -> Player | None:
        """Найти игрока по имени."""
        return self._casino_balance.get_player(name)
