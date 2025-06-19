"""Launcher."""
import json
from pathlib import Path

from ex1.code import run as run_ex1
from ex2.code import run as run_ex2
from ex3.code import run as run_ex3
from ex4.code import run as run_ex4
from ex5.code import run as run_ex5
from ex6.code import run as run_ex6
from ex7.code import run as run_ex7
from logger import logger

CONFIG_PATH = Path("Config.json")
BASE_EXO_DIR = "ex"

def load_config():
    with Path.open(CONFIG_PATH) as file:
        return json.load(file)

def main():
    config = load_config()

    options = [
        "Exercice 1",
        "Exercice 2",
        "Exercice 3",
        "Exercice 4",
        "Exercice 5",
        "Exercice 6",
        "Exercice 7",
        "Quitter",
    ]

    while True:
        print("📘 Menu")
        for i, opt in enumerate(options):
            print(f"{i + 1}. {opt}")

        choice = input("\n👉 Choississez une option : ")

        if choice == "1":
            run_ex1(config.get("ex1", {}))
        elif choice == "2":
            run_ex2(config.get("ex2", {}))
        elif choice == "3":
            run_ex3(config.get("ex3", {}))
        elif choice == "4":
            run_ex4(config.get("ex4", {}))
        elif choice == "5":
            run_ex5(config.get("ex5", {}))
        elif choice == "6":
            run_ex6(config.get("ex6", {}))
        elif choice == "7":
            run_ex7(config.get("ex7", {}))
        elif choice == "8":
            logger.info("À bientôt !")
            break
        else:
            logger.error("❌ Option invalide")

        input("\nAppuyez sur Entrée pour revenir au menu...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        logger.info("Interruption manuelle, à bientôt !")
