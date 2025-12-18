from __future__ import annotations

from src.collections.casinoBalance import CasinoBalance
from src.entities.player import Player


class PlayerCollection:
    """Списковая коллекция, использует CasinoBalance внутри"""

    def __init__(self, casino_balance: CasinoBalance | None = None):
        """
        Инициализация коллекции

        Args:
            casino_balance: Ссылка на словарную коллекцию (опционально)
        """
        if casino_balance is None:
            self._casino_balance = CasinoBalance()
        else:
            self._casino_balance = casino_balance

        # Для быстрого доступа по индексу
        self._player_names = []

    @property
    def casino_balance(self) -> CasinoBalance:
        return self._casino_balance

    def _update_index(self):
        """Обновить индекс имён для быстрого доступа"""
        self._player_names = list(self._casino_balance.keys())

    def __getitem__(self, key: int | slice) -> Player | PlayerCollection:
        """Доступ по индексу или срезу"""
        self._update_index()

        if isinstance(key, slice):
            # Создаём новую коллекцию для среза
            new_collection = PlayerCollection(self._casino_balance)
            new_collection._player_names = self._player_names[key]
            return new_collection
        elif isinstance(key, int):
            player_name = self._player_names[key]
            return self._casino_balance.get_player(player_name)
        else:
            raise TypeError(f"Индекс должен быть int или slice, а не {type(key).__name__}")

    def __len__(self) -> int:
        """Количество игроков"""
        return len(self._casino_balance)

    def __iter__(self):
        """Итерация по игрокам"""
        return iter(self._casino_balance.values())

    def __contains__(self, item: Player | str) -> bool:
        """Проверка наличия игрока"""
        if isinstance(item, Player):
            return item.name in self._casino_balance
        elif isinstance(item, str):
            return item in self._casino_balance
        return False

    def add_player(self, player: Player):
        """Добавить игрока"""
        self._casino_balance.register_player(player)
        self._update_index()

    def remove_player(self, identifier: Player | str) -> Player | None:
        """Удалить игрока"""
        if isinstance(identifier, Player):
            player_name = identifier.name
        elif isinstance(identifier, str):
            player_name = identifier
        else:
            return None

        player = self._casino_balance.remove_player(player_name)
        if player:
            self._update_index()
        return player

    def find_player(self, name: str) -> Player | None:
        """Найти игрока по имени"""
        return self._casino_balance.get_player(name)

