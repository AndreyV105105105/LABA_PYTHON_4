from src.entities.casino import Casino
from src.entities.player import Player
from src.entities.goose import Goose, WarGoose, HonkGoose

def _create_demo_casino() -> Casino:
    casino = Casino()

    # Игроки (можно заменить на свои имена/балансы)
    casino.register_player(Player("Андрей Вольвач", 1000))
    casino.register_player(Player("Николай Сергеевич", 1000))
    casino.register_player(Player("Самир Ахмед", 1000))

    # Гуси
    casino.register_goose(Goose("Салага", honk_volume=3))
    casino.register_goose(WarGoose("Бедолага", honk_volume=2))
    casino.register_goose(HonkGoose("Жучара", honk_volume=10))

    return casino


def run() -> None:
    print("Казино и гуси: симуляция")
    print("Введите количество шагов (steps) и необязательный seed.")
    print("Если seed задан, последовательность событий будет воспроизводимой.")

    try:
        raw_steps = input("steps (по умолчанию 20): ").strip()
        steps = 20 if raw_steps == "" else int(raw_steps)
        if steps <= 0:
            raise ValueError("steps должен быть больше 0")

        raw_seed = input("seed (пусто = случайно): ").strip()
        seed = None if raw_seed == "" else int(raw_seed)
        print()
        casino = _create_demo_casino()
        casino.run_simulation(steps=steps, seed=seed)

    except ValueError as e:
        print(f"[ERROR] Некорректный ввод: {e}")
    except KeyboardInterrupt:
        print("\n[STOP] Симуляция остановлена пользователем.")
    except Exception as e:
        print(f"[ERROR] Непредвиденная ошибка: {type(e).__name__}: {e}")
