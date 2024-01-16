from utils import randbool
from utils import randcell
from utils import randcell2
from constants import FOREST_CHANCE, MAX_FOREST_CHANCE, RIVER_LENGTH, UPGRADE_COST, LIFE_COST, CELL_TYPES, TREE_BONUS

# Определение типов клеток и связанных констант
#  0 - поле
#  1 - дерево
#  2 - река
#  3 - госпиталь
#  4 - апгрейд шоп
#  5 - огонь

class Map:
    def __init__(self, w, h):
        # Инициализация карты с указанными размерами и генерацией различных элементов
        self.w = w
        self.h = h
        self.cells = [[0 for i in range(w)] for j in range(h)]
        self.generate_forest(FOREST_CHANCE, MAX_FOREST_CHANCE)
        self.generate_river(RIVER_LENGTH)
        self.generate_river(RIVER_LENGTH)
        self.generate_upgrade_shop()
        self.generate_hospital()

    def check_bounds(self, x, y):
        # Проверка, находится ли точка в пределах карты
        return 0 <= x < self.h and 0 <= y < self.w

    def print_map(self, helico, clouds):
        # Вывод карты на экран с учетом вертолета и облаков
        print("⬛" * (self.w + 2))
        for ri, row in enumerate(self.cells):
            print("⬛", end="")
            for ci, cell in enumerate(row):
                if (clouds.cells[ri][ci] == 1):
                    print("⛅️", end="")
                elif (clouds.cells[ri][ci] == 2):
                    print("⚡", end="")
                elif (helico.x == ri and helico.y == ci):
                    print("🚁", end="")
                elif (cell >= 0 and cell < len(CELL_TYPES)):
                    print(CELL_TYPES[cell], end="")
            print("⬛")
        print("⬛" * (self.w + 2))

    def generate_river(self, l):
        # Генерация реки на карте
        # l - длина реки
        # Использует случайные координаты для начала реки и продолжает ее на l клеток
        # Код проверяет границы карты и корректно обрабатывает выход за пределы карты
        rc = randcell(self.w, self.h)
        rx, ry = rc[0], rc[1]

        if self.check_bounds(rx, ry):
            self.cells[rx][ry] = 2
        else:
            return

        while l > 0:
            rc2 = randcell2(rx, ry)
            rx2, ry2 = rc2[0], rc2[1]
            if self.check_bounds(rx2, ry2):
                self.cells[rx2][ry2] = 2
                rx, ry = rx2, ry2
                l -= 1
            else:
                break

    def generate_forest(self, r, mxr):
        # Генерация леса на карте
        # r - шанс появления дерева в клетке (меньше значение - больше деревьев)
        # mxr - максимальный шанс для создания разнообразия
        # Использует случайные числа для определения наличия дерева в каждой клетке
        for ri in range(self.h):
            for ci in range(self.w):
                if randbool(r, mxr):
                    self.cells[ri][ci] = 1

    def generate_tree(self):
        # Генерация дерева в случайной клетке
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        if self.check_bounds(cx, cy) and self.cells[cx][cy] == 0:
            self.cells[cx][cy] = 1

    def generate_upgrade_shop(self):
        # Генерация магазина улучшений в случайной клетке
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        if self.check_bounds(cx, cy):
            self.cells[cx][cy] = 4

    def generate_hospital(self):
        # Генерация госпиталя в случайной клетке (не на магазине улучшений)
        while True:
            c = randcell(self.w, self.h)
            cx, cy = c[0], c[1]
            if self.check_bounds(cx, cy) and self.cells[cx][cy] != 4:
                self.cells[cx][cy] = 3
                break

    def add_fire(self):
        # Добавление огня в случайной клетке с деревом
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        if self.check_bounds(cx, cy) and self.cells[cx][cy] == 1:
            self.cells[cx][cy] = 5

    def update_fires(self):
        # Обновление состояний клеток с огнем и добавление новых огней
        # Сбрасывает состояние клеток с огнем и добавляет новые огни в случайные клетки
        for ri in range(self.h):
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if cell == 5:
                    self.cells[ri][ci] = 0
        for i in range(10):
            self.add_fire()

    def process_helicopter(self, helico, clouds):
        # Обработка состояния вертолета в зависимости от типа клетки и облаков
        # Обновляет состояние вертолета, проверяя тип клетки и наличие облаков в его текущей позиции
        # Включает логику для топлива, счета, улучшений, жизней и геймовера
        if helico.x < 0 or helico.y < 0 or helico.x >= self.h or helico.y >= self.w:
            return  # Вертолет за пределами карты, не обрабатываем

        c = self.cells[helico.x][helico.y]
        d = clouds.cells[helico.x][helico.y]
        if (c == 2):
            helico.tank = helico.mxtank
        if (c == 5 and helico.tank > 0):
            helico.tank -= 1
            helico.score += TREE_BONUS
            self.cells[helico.x][helico.y] = 1
        if (c == 4 and helico.score >= UPGRADE_COST):
            helico.mxtank += 1
            helico.score -= UPGRADE_COST
        if (c == 3 and helico.score >= LIFE_COST):
            helico.lives += 10
            helico.score -= LIFE_COST
        if (d == 2):
            helico.lives -= 1
            if (helico.lives == 0):
                helico.game_over()

    def export_data(self):
        # Экспорт данных карты в виде словаря
        return {"cells": self.cells}

    def import_data(self, data):
        # Импорт данных карты из словаря
        # Если данные отсутствуют, создается новая карта
        self.cells = data["cells"] or [[0 for i in range(self.w)] for j in range(self.h)]