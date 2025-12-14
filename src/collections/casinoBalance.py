from src.entities.player import Player


class CasinoBalance:
    """
    Словарная коллекция для работы с балансами игроков через объекты Player
    Ключ: имя игрока (str)
    Значение: объект Player
    """

    def __init__(self):
        """
        Инициализация коллекции балансов
        """
        self._players: dict[str, Player] = {}
        self._transaction_log: list = []

    def __getitem__(self, player_name: str) -> int:
        """
        Получить баланс игрока по имени

        Args:
            player_name: Имя игрока

        Returns:
            Текущий баланс игрока

        Raises:
            KeyError: если игрок не найден
        """
        if player_name not in self._players:
            raise KeyError(f"Игрок '{player_name}' не найден")
        return self._players[player_name].balance

    def __setitem__(self, player_name: str, new_balance: int):
        """
        Установить баланс игрока

        Args:
            player_name: Имя игрока
            new_balance: Новый баланс

        Raises:
            KeyError: если игрок не найден
        """
        if player_name not in self._players:
            raise KeyError(f"Нельзя установить баланс - игрок '{player_name}' не найден")

        player = self._players[player_name]
        old_balance = player.balance

        player.balance = new_balance

        # Логируем изменение
        self._log_transaction(player_name, old_balance, player.balance)

    def __delitem__(self, player_name: str):
        """Удалить игрока из коллекции"""
        if player_name in self._players:
            # Логируем удаление
            self._log_transaction(
                player_name,
                self._players[player_name].balance,
                0,
                action="УДАЛЕНИЕ"
            )
            del self._players[player_name]

    def __len__(self) -> int:
        """Количество игроков в коллекции"""
        return len(self._players)

    def __contains__(self, player_name: str) -> bool:
        """Проверка наличия игрока по имени"""
        return player_name in self._players

    def __repr__(self) -> str:
        """Официальное строковое представление"""
        items = [f"'{k}': Player(balance={v.balance})" for k, v in self._players.items()]
        return f"CasinoBalance({{{', '.join(items)}}})"

    def __str__(self) -> str:
        """Пользовательское строковое представление"""
        if not self._players:
            return "Балансы казино (пусто)"

        result = ["Балансы казино:"]
        sorted_items = sorted(
            self._players.items(),
            key=lambda x: x[1].balance,
            reverse=True
        )

        for i, (player_name, player) in enumerate(sorted_items, 1):
            bankrupt = " (БАНКРОТ)" if player.is_bankrupt else ""
            result.append(f"{player_name}: {player.balance} монет{bankrupt}")

        result.append(f"\nВсего игроков: {len(self)}")
        result.append(f"Общая сумма: {self.get_total_balance()} монет")

        return "\n".join(result)

    def keys(self):
        """Ключи коллекции (имена игроков)"""
        return self._players.keys()

    def values(self):
        """Значения коллекции (объекты Player)"""
        return self._players.values()

    def items(self):
        """Пары ключ-значение"""
        return self._players.items()

    def register_player(self, player: Player):
        """
        Зарегистрировать игрока в казино

        Args:
            player: Объект Player

        Raises:
            ValueError: если игрок уже зарегистрирован
        """
        if player.name in self._players:
            raise ValueError(f"Игрок '{player.name}' уже зарегистрирован")

        self._players[player.name] = player
        self._log_transaction(player.name, 0, player.balance, "РЕГИСТРАЦИЯ")

    def get_player(self, player_name: str) -> Player | None:
        """Получить объект Player по имени"""
        return self._players.get(player_name)

    def remove_player(self, player_name: str) -> Player | None:
        """Удалить игрока и вернуть его объект"""
        if player_name in self._players:
            player = self._players[player_name]
            del self._players[player_name]
            self._log_transaction(
                player_name,
                player.balance,
                0,
                action="УДАЛЕНИЕ"
            )
            return player
        return None

    def receive_cash(self, player_name: str, amount: int) -> bool:
        """
        Пополнить баланс игрока

        Args:
            player_name: Имя игрока
            amount: Сумма пополнения

        Returns:
            True если успешно, False если игрок не найден
        """
        if player_name not in self._players:
            return False

        player = self._players[player_name]
        old_balance = player.balance

        # Используем метод Player для получения денег
        player.receive_cash(amount)

        self._log_transaction(player_name, old_balance, player.balance)
        return True

    def make_bet(self, player_name: str, amount: int) -> bool:
        """
        Сделать ставку

        Args:
            player_name: Имя игрока
            amount: Сумма снятия

        Returns:
            True если успешно, False если недостаточно средств или игрок не найден
        """
        if player_name not in self._players:
            return False

        player = self._players[player_name]
        old_balance = player.balance

        # Используем метод Player для ставки
        success = player.make_bet(amount)

        if success:
            self._log_transaction(player_name, old_balance, player.balance)

        return success

    def _log_transaction(self, player_name: str, old_balance: int,
                         new_balance: int, action: str = "ИЗМЕНЕНИЕ"):
        """Логирование изменения баланса"""
        change = new_balance - old_balance

        log_entry = {
            'player': player_name,
            'old_balance': old_balance,
            'new_balance': new_balance,
            'change': change,
            'action': action,
            'timestamp': f"Шаг {len(self._transaction_log) + 1}"
        }

        self._transaction_log.append(log_entry)

        # Вывод в консоль
        change_str = f"+{change}" if change > 0 else str(change)
        print(f"[BALANCE] {action}: {player_name}: {old_balance} → {new_balance} ({change_str})")

    def get_total_balance(self) -> int:
        """Получить общую сумму всех балансов"""
        return sum(player.balance for player in self._players.values())

    def get_average_balance(self) -> float:
        """Получить средний баланс"""
        if not self._players:
            return 0.0
        return self.get_total_balance() / len(self._players)

    def get_transaction_log(self, player_name: str | None = None) -> list:
        """Получить историю транзакций"""
        if player_name is None:
            return self._transaction_log.copy()
        return [entry for entry in self._transaction_log
                if entry['player'] == player_name]


