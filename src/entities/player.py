class Player:
    def __init__(self, name: str, initial_balance: int = 1000):
        self.name = name
        self._balance = max(0, initial_balance)
        self._is_bankrupt = (self._balance == 0)

    @property
    def balance(self) -> int:
        return self._balance

    @property
    def is_bankrupt(self) -> bool:
        return self._is_bankrupt

    @balance.setter
    def balance(self, new_balance: int):
        if new_balance < 0:
            self._balance = 0
            self._is_bankrupt = True
        else:
            self._balance = new_balance
            # Снимаем флаг банкротства, если баланс стал положительным
            if new_balance > 0:
                self._is_bankrupt = False
            # Или устанавливаем, если баланс стал 0
            elif new_balance == 0:
                self._is_bankrupt = True

    def make_bet(self, amount: int) -> bool:
        """Сделать ставку указанной суммы"""
        if self._is_bankrupt:
            return False
        elif amount > self._balance:
            return False
        elif amount <= 0:
            raise ValueError("Сумма ставки должна быть больше 0")
        else:
            self._balance -= amount
            # Если баланс обнулился после ставки - банкротство
            if self._balance == 0:
                self._is_bankrupt = True
            return True

    def receive_cash(self, cash: int) -> None:
        """Получить деньги"""
        if cash <= 0:
            raise ValueError("Получаемая сумма должна быть больше 0")

        old_balance = self._balance
        self._balance += cash

        # Выход из банкротства при получении денег
        if old_balance == 0 and cash > 0:
            self._is_bankrupt = False

    def go_bankrupt(self) -> None:
        """Принудительно объявить банкротом"""
        self._balance = 0
        self._is_bankrupt = True

    def __str__(self) -> str:
        if self._is_bankrupt:
            return f"Игрок {self.name} (БАНКРОТ)"
        return f"Игрок {self.name} (баланс: {self._balance})"

    def __repr__(self) -> str:
        return f"Player('{self.name}', balance={self._balance})"