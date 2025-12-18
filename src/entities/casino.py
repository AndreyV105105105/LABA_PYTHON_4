import random

from src.entities.player import Player
from src.entities.goose import Goose, WarGoose, HonkGoose
from src.collections.casinoBalance import CasinoBalance
from src.collections.player_collection import PlayerCollection


class Casino:
    """
    Казино: содержит коллекции игроков, гусей и денежные потоки.
    Делает один шаг симуляции (случайное событие) и печатает лог.
    """

    def __init__(self, players: PlayerCollection | None = None, casino_balance: CasinoBalance | None = None):
        if casino_balance is not None:
            self._casino_balance = casino_balance
            self._players = players if players is not None else PlayerCollection(casino_balance)
        else:
            self._players = players if players is not None else PlayerCollection()
            # забираем баланс из коллекции игроков
            self._casino_balance = self._players.casino_balance


        self._geese = []
        self._goose_income = {} # доходы гусей по имени
        self._casino_profit = 0 # прибыль казино (может быть отрицательной)

    @property
    def players(self) -> PlayerCollection:
        return self._players

    @property
    def casino_balance(self) -> CasinoBalance:
        return self._casino_balance

    @property
    def geese(self) -> list[Goose]:
        return self._geese

    @property
    def casino_profit(self) -> int:
        return self._casino_profit

    @property
    def goose_income(self) -> dict[str, int]:
        # отдаем копию, чтобы снаружи не ломали инварианты
        return dict(self._goose_income)

    def register_player(self, player: Player) -> None:
        self._players.add_player(player)

    def register_goose(self, goose: Goose) -> None:
        self._geese.append(goose)
        self._goose_income.setdefault(goose.name, 0)
        print(f"[CASINO] Зарегистрирован гусь: {goose}")

    def _active_players(self) -> list[Player]:
        return [p for p in self._players if not p.is_bankrupt]

    def _random_player(self, allow_bankrupt: bool = False) -> Player | None:
        if len(self._players) == 0:
            return None
        if allow_bankrupt:
            return random.choice(list(self._players))
        candidates = self._active_players()
        return random.choice(candidates) if candidates else None

    def _random_goose(self) -> Goose | None:
        if not self._geese:
            return None
        return random.choice(self._geese)

    def _add_goose_income(self, goose: Goose, amount: int) -> None:
        if amount <= 0:
            return
        self._goose_income[goose.name] = self._goose_income.get(goose.name, 0) + amount
        print(f"[GOOSE-INCOME] {goose.name}: + {amount} (итого {self._goose_income[goose.name]})")

    def player_bet_round(self) -> None:
        """
        Игрок делает ставку: либо выигрывает, либо проигрывает.
        Деньги снимаются/начисляются через CasinoBalance, чтобы было логирование.
        """
        player = self._random_player()
        if player is None:
            print("[STEP] Нет активных игроков для ставки.")
            return

        bet = random.randint(10, 200)
        print(f"[STEP] Ставка: {player.name} пытается поставить {bet} монет.")

        success = self._casino_balance.make_bet(player.name, bet)
        if not success:
            print(f"[STEP] Ставка не удалась: {player.name} (недостаточно средств или игрок не найден).")
            return

        # казино получило ставку
        self._casino_profit += bet

        # 34% шанс выиграть (тогда казино платит x2 от ставки, чистая прибыль казино -bet)
        if random.random() < 0.34:
            payout = bet * 2
            self._casino_balance.receive_cash(player.name, payout)
            self._casino_profit -= payout
            print(f"[STEP] {player.name} выиграл! Выплата {payout}.")
        else:
            print(f"[STEP] {player.name} проиграл ставку {bet}.")

    def goose_attack_or_honk(self) -> None:
        """
        Событие с гусём:
        - WarGoose атакует (крадёт)
        - HonkGoose кричит и меняет баланс
        - базовый Goose пытается украсть
        """
        goose = self._random_goose()
        player = self._random_player()
        if goose is None or player is None:
            print("[STEP] Нет гусей или активных игроков для события с гусём.")
            return

        print(f"[STEP] Гусь выбран: {goose.name} ({goose.goose_type}), цель: {player.name}")

        if isinstance(goose, (WarGoose, HonkGoose)):
            delta, description = goose(player)
            print(f"[STEP] {description}")

            # Обновим денежные потоки:
            if isinstance(goose, WarGoose) and delta > 0:
                # украл у игрока -> доход гуся
                self._add_goose_income(goose, delta)
            elif isinstance(goose, HonkGoose):
                # delta > 0: игрок получил деньги
                # delta < 0: игрок потерял деньги
                if delta > 0:
                    self._casino_profit -= delta
                elif delta < 0:
                    self._casino_profit += (-delta)
        else:
            stolen, description = goose.steal(player)
            print(f"[STEP] {description}")
            if stolen > 0:
                self._add_goose_income(goose, stolen)

    def goose_toggle_activity(self) -> None:
        """Случайно активировать/деактивировать гуся"""
        goose = self._random_goose()
        if goose is None:
            print("[STEP] Нет гусей для переключения активности.")
            return

        if goose.is_active:
            goose.deactivate()
            print(f"[STEP] Гусь {goose.name} деактивирован.")
        else:
            goose.activate()
            print(f"[STEP] Гусь {goose.name} активирован.")

    def panic_bankrupt(self) -> None:
        """Случайная паника: игрок теряет всё."""
        player = self._random_player()
        if player is None:
            print("[STEP] Нет активных игроков для паники.")
            return

        old = player.balance
        player.go_bankrupt()
        self._casino_profit += old
        print(f"[STEP] Паника! {player.name} проиграл всё ({old} -> 0).")

    def step(self) -> None:
        """
        Один шаг симуляции: ровно одно случайное событие + лог в консоль.
        """
        if random.random() < 0.1:
            self.panic_bankrupt()
        else:
            events = [
                self.player_bet_round,
                self.goose_attack_or_honk,
                self.goose_toggle_activity
            ]
            random.choice(events)()
        print(f"[STATE] Прибыль казино: {self._casino_profit}")
        # print(f"[STATE] Игроков: {len(self._players)}, гусей: {len(self._geese)}")

    def run_simulation(self, steps: int = 20, seed: int | None = None) -> None:
        """
        Запуск симуляции на steps шагов, с seed для воспроизводимости.
        """
        if steps <= 0:
            raise ValueError("steps должен быть > 0")
        if seed is not None:
            random.seed(seed)

        print(f"[SIM] Запуск симуляции: steps={steps}, seed={seed}")
        for i in range(1, steps + 1):
            print(f"\nШАГ {i}")
            self.step()

    def __str__(self) -> str:
        return f"Casino(players={len(self._players)}, geese={len(self._geese)}, profit={self._casino_profit})"

    def __repr__(self) -> str:
        return f"Casino(players={len(self._players)}, geese={len(self._geese)}, profit={self._casino_profit})"
