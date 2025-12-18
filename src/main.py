from src.additional_functions.run import run


def main():
    """
    Главная функция приложения.
    Запускает основной цикл программы.
    """
    print("\nГЛАВНОЕ МЕНЮ")
    try:
        # Запускаем основной цикл программы
        run()
    except Exception as err:
        # Обрабатываем возможные ошибки в основном цикле
        print(f"Произошла ошибка: {err}")
        return False


if __name__ == "__main__":
    # Запускаем приложение при прямом вызове файла
    main()