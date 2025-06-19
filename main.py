"""Launcher."""
import json
from pathlib import Path
from typing import Any

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

def load_config() -> dict[str, Any]:
    """Load the configuration from the JSON file."""
    with Path.open(CONFIG_PATH) as file:
        return json.load(file)

def display_menu(options: list[str]) -> None:
    """Display the menu options."""
    print("📘 Menu") #noqa: T201
    for i, opt in enumerate(options, start=1):
        print(f"{i}. {opt}") #noqa: T201

def handle_choice(choice: str, config: dict[str, Any]) -> bool:
    """Handle the user's choice from the menu."""
    runs = {
        "1": run_ex1,
        "2": run_ex2,
        "3": run_ex3,
        "4": run_ex4,
        "5": run_ex5,
        "6": run_ex6,
        "7": run_ex7,
    }

    if choice in runs:
        runs[choice](config.get(f"ex{choice}", {}))
        return True
    if choice == "8":
        logger.info("À bientôt !")
        return False
    logger.error("❌ Option invalide")
    return True

def main() -> None:
    """Run the menu and handle user choices."""
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

    running = True
    while running:
        display_menu(options)
        choice = input("\n👉 Choississez une option : ")
        running = handle_choice(choice, config)
        if running:
            input("\nAppuyez sur Entrée pour revenir au menu...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print() #noqa: T201
        logger.info("Interruption manuelle, à bientôt !")
