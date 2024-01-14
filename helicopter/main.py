# main.py
from game import Game

def main():
    # Создаем объект игры
    game = Game()

    # Запускаем основной игровой цикл
    while not game.game_over:
        # Обновляем состояние игры
        game.update()

if __name__ == "__main__":
    main()
