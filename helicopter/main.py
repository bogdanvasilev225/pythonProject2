from pynput import keyboard
from clouds import Clouds
from map import Map
import time
import os
import json
from helicopter import Helicopter as Helico

# Константы времени и размера карты
TICK_SLEEP = 0.05
CLOUDS_UPDATE = 100
TREE_UPDATE = 30
FIRE_UPDATE = 75
MAP_W, MAP_H = 20, 10

# Инициализация объектов (карты, облаков и вертолета)
field = Map(MAP_W, MAP_H)
clouds = Clouds(MAP_W, MAP_H)
helico = Helico(MAP_W, MAP_H)
tick = 1  # Счетчик тиков


# Словарь для определения движения вертолета по клавишам
MOVES = {'w': (-1, 0), 'd': (0, 1), 's': (1, 0), 'a': (0, -1)}
# Клавиши для сохранения и загрузки игры
# f - сохранение, g - восстановление

# Функция сохранения текущего состояния игры в файл
def save_game():
    try:
        data = {"helicopter": helico.export_data(),
                "clouds": clouds.export_data(),
                "field": field.export_data(),
                "tick": tick}

        with open("level.json", "w") as lwl:
            json.dump(data, lwl)
    except (IOError, PermissionError) as e:
        print(f"Error saving game: {e}")


# Функция загрузки состояния игры из файла
def load_game():
    try:
        with open("level.json", "r") as lvl:
            data = json.load(lvl)
            tick = data.get("tick", 1)
            helico.import_data(data.get("helicopter", {}))
            field.import_data(data.get("field", {}))
            clouds.import_data(data.get("clouds", {}))
    except FileNotFoundError:
        print("No saved game found.")
        field.generate_tree()
        clouds.update()


# Функция обработки нажатий клавиш
def process_key(key):
    global helico, tick, clouds, field
    if isinstance(key, keyboard.KeyCode):
        c = key.char.lower()

        # обработка движения вертолета
        if c in MOVES.keys():
            dx, dy = MOVES[c][0], MOVES[c][1]
            helico.move(dx, dy)

        # сохранение игры
        elif c == "f":
            save_game()

        # загрузка игры
        elif c == "g":
            load_game()

# Начало слушателя клавиш
listener = keyboard.Listener(
    on_press=None,
    on_release=process_key,)
listener.start()


def update_game_state():
    # Обновление состояния игры
    field.process_helicopter(helico, clouds)
    helico.print_stats()
    field.print_map(helico, clouds)
    print("TICK", tick)
    


def main_game_loop():
    global tick  # Добавьте эту строку
    # Основной игровой цикл
    while True:
        os.system("cls")
        update_game_state()
        tick += 1
        time.sleep(TICK_SLEEP)

        # Обновление состояний в зависимости от тиков
        if tick % TREE_UPDATE == 0:
            field.generate_tree()
        if tick % FIRE_UPDATE == 0:
            field.update_fires()
        if tick % CLOUDS_UPDATE == 0:
            clouds.update()

if __name__ == "__main__":
    main_game_loop()
