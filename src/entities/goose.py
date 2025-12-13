import random
from typing import Optional
from src.entities.player import Player


class Goose:
    """Базовый класс для всех гусей"""

    def __init__(self, name: str, honk_volume: int = 1):
        """
        Инициализация гуся

        Args:
            name: Имя гуся
            honk_volume: Громкость крика (1-10, по умолчанию 1)
        """
        self._name = name
        self._honk_volume = max(1, min(10, honk_volume))  # Ограничение 1-10
        self._is_active = True

    @property
    def name(self) -> str:
        """Имя гуся (только для чтения)"""
        return self._name

    @property
    def honk_volume(self) -> int:
        """Громкость крика (только для чтения)"""
        return self._honk_volume

    @property
    def is_active(self) -> bool:
        """Активен ли гусь (может выполнять действия)"""
        return self._is_active

    @property
    def goose_type(self) -> str:
        """Тип гуся (будет переопределен в подклассах)"""
        return "BaseGoose"

    def activate(self) -> None:
        """Активировать гуся"""
        self._is_active = True

    def deactivate(self) -> None:
        """Деактивировать гуся (не может выполнять действия)"""
        self._is_active = False

    def honk(self) -> str:
        """Издать базовый крик"""
        if not self._is_active:
            return f"{self._name} молчит (неактивен)"

        volume_description = { # признаюсь, значения словаря нагенерил
            1: "едва слышный писк",
            2: "тихое ворчание",
            3: "средней громкости кряканье",
            4: "нормальное гоготание",
            5: "громкое возмущение",
            6: "резкий пронзительный крик",
            7: "мощный устрашающий рёв",
            8: "невероятно громкий ор",
            9: "разрывающий барабанные перепонки вопль",
            10: "нечеловеческий ультразвуковой визг"
        }

        description = volume_description.get(self._honk_volume, "крик")
        return f"Гусь {self._name} издаёт {description} (громкость: {self._honk_volume})"

    def steal(self, player: Player) -> tuple[int, str]:
        """
        Попытаться украсть деньги у игрока (базовая реализация)

        Args:
            player: Целевой игрок

        Returns:
            Кортеж: (украденная сумма, описание действия)
        """
        if not self._is_active:
            return 0, f"{self._name} неактивен"

        if player.is_bankrupt:
            return 0, f"Игрок {player.name} банкрот"

        # Базовый гусь с 50% шансом крадёт 10 монет
        if random.random() < 0.5:
            steal_amount = 10
            if steal_amount > player.balance:
                steal_amount = player.balance

            if steal_amount > 0 and player.make_bet(steal_amount):
                return steal_amount, f"Гусь {self._name} украл {steal_amount} монет у {player.name}"

        return 0, f"Гусь {self._name} пытался украсть у {player.name}, но не смог"

    # Магические методы
    def __call__(self) -> str:
        """Вызов гуся как функции - издает крик"""
        return self.honk()

    def __str__(self) -> str:
        """Строковое представление для пользователя"""
        if self._is_active:
            status = 'Активен'
        else:
            status = 'Неактивен'
        return f"{status} Гусь {self._name} ({self.goose_type}, громкость: {self._honk_volume})"

    def __repr__(self) -> str:
        """Официальное строковое представление для отладки"""
        return f"Goose(name='{self._name}', honk_volume={self._honk_volume})"


class HonkGoose(Goose):
    """Гусь-крикун - специальный гусь с уникальным криком"""

    def __init__(self, name: str, honk_volume: int = 10):
        """
        Инициализация гуся-крикуна

        Args:
            name: Имя гуся
            honk_volume: Громкость крика (1-10, по умолчанию 10 - максимальная)
        """
        super().__init__(name, honk_volume)
        self._special_power = self._honk_volume * 10  # Сила эффекта зависит от громкости

    @property
    def goose_type(self) -> str:
        """Тип гуся (переопределено)"""
        return "HonkGoose"

    @property
    def special_power(self) -> int:
        """Сила специального эффекта"""
        return self._special_power

    def honk(self, target_player: Optional[Player] = None) -> tuple[int, str]:
        """
        Специальный крик с эффектом

        Args:
            target_player: Игрок, на которого направлен крик (опционально)

        Returns:
            Кортеж: (описание крика, изменение баланса игрока)
        """
        if not self._is_active:
            return 0, f"{self._name} молчит (неактивен)"

        # Базовое описание крика
        base_description = super().honk()

        if target_player is None:
            return 0, base_description

        # Определяем тип эффекта
        effect_roll = random.random()

        if effect_roll < 0.2:  # 20% - положительный эффект
            amount = random.randint(5, self._special_power)
            target_player.receive_cash(amount)
            return amount, f"{base_description} и дарит {amount} монет игроку {target_player.name}!"

        elif effect_roll < 0.6:  # 40% - отрицательный эффект
            amount = random.randint(5, self._special_power // 2)
            if target_player.make_bet(amount):
                return -amount, f"{base_description} и забирает {amount} монет у игрока {target_player.name}!"
            else:
                return 0, f"{base_description}, но у игрока {target_player.name} нет денег!"

        else:  # 20% - особый эффект
            special_effect = random.choice([
                self._cause_panic,
                self._attract_money
            ])
            return special_effect(target_player, base_description)

    def _cause_panic(self, player: Player, description: str) -> tuple[int, str]:
        """Вызвать панику у игрока"""
        panic_amount = random.randint(20, 100)
        if player.make_bet(panic_amount):
            return -panic_amount, f"{description} и вызывает панику! {player.name} теряет {panic_amount} монет!"
        return 0, f"{description} и пытается вызвать панику, но у {player.name} нет денег!"

    def _attract_money(self, player: Player, description: str) -> tuple[int, str]:
        """Дать игроку халявные деньги"""
        attracted_amount = random.randint(20, 100)
        player.receive_cash(attracted_amount)
        return attracted_amount, f"{description} и сносит яйцо для {player.name}, в котором оказывается {attracted_amount} монет!"

    def __call__(self, target_player: Optional[Player] = None) -> tuple[int, str]:
        """
        Магический метод для вызова гуся как функции

        Args:
            target_player: Игрок, на которого направлен крик

        Returns:
            Кортеж: (изменение баланса игрока, описание крика)
        """
        if target_player is None:
            return 0, f"{self._name} готов к крику, но нет цели"
        return self.honk(target_player)

    def __str__(self) -> str:
        """Строковое представление"""
        if self._is_active:
            status = "Активен"
        else:
            status = "Неактивен"

        return f"{status} Гусь-крикун {self._name} [Громкость: {self._honk_volume}]"

    def __repr__(self) -> str:
        """Официальное строковое представление"""
        return f"HonkGoose(name='{self._name}', honk_volume={self._honk_volume})"



class WarGoose(Goose):
    """Военный гусь - атакует игроков с гарантированной кражей"""
    def __init__(self, name: str, honk_volume: int = 1):
        """
        Инициализация военного гуся

        Args:
            name: Имя гуся
            honk_volume: Громкость крика (по умолчанию 1)
        """
        super().__init__(name, honk_volume)

    @property
    def goose_type(self) -> str:
        return "WarGoose"

    def honk(self) -> str:
        """Военный гусь издаёт боевой клич"""
        if not self._is_active:
            return f"{self._name} молчит (неактивен)"
        return f"{self._name} издаёт боевое ГА-ГА!"

    def steal(self, player: Player) -> tuple[int, str]:
        """
        Гарантированно украсть деньги у игрока

        Args:
            player: Цель кражи(игрок)

        Returns:
            Кортеж: (украденная сумма, описание действия)
        """
        if not self._is_active:
            return 0, f"{self._name} неактивен"

        if player.is_bankrupt:
            return 0, f"Игрок {player.name} банкрот"

        # Военный гусь крадёт гарантированно случайное число от 10 до 50 * на силу крика
        steal_amount = random.randint(10, 50) * self.honk_volume
        if steal_amount > player.balance:
            steal_amount = player.balance

        if steal_amount > 0 and player.make_bet(steal_amount):
            return steal_amount, f"Гусь {self._name} атаковал и украл {steal_amount} монет у {player.name}"

        return 0, f"Гусь {self._name} пытался украсть у {player.name}, но не смог"


    def __call__(self, target_player: Optional[Player] = None) -> tuple[int, str]:
        """
        Магический метод для вызова гуся как функции

        Args:
            target_player: Игрок, на которого направлена атака

        Returns:
            Кортеж: (изменение баланса игрока, описание атаки)
        """
        if target_player is None:
            return 0, f"{self._name} готов к атаке, но нет цели"
        return self.steal(target_player)

    def __str__(self) -> str:
        """Строковое представление"""
        if self._is_active:
            status = "Активен"
        else:
            status = "Неактивен"

        return f"{status} Военный гусь {self._name} [Громкость: {self._honk_volume}]"

    def __repr__(self) -> str:
        """Официальное строковое представление"""
        return f"WarGoose(name='{self._name}', honk_volume={self._honk_volume})"