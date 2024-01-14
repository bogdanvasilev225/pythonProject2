# file_operations.py
import pickle

def save_game(game):
    # Метод сохранения игры в файл
    with open("save_game.pkl", "wb") as f:
        pickle.dump(game, f)

def load_game():
    # Метод загрузки игры из файла
    with open("save_game.pkl", "rb") as f:
        return pickle.load(f)
