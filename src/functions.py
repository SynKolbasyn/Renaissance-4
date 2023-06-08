import ujson
import os

import player


def get_dict_from_json(file_name: str) -> dict:
    with open(file_name, "r", encoding="utf-8") as file:
        return ujson.load(file)


def create_new_account(ID: int, login: str, name: str) -> player.Player:
    account = player.Player(ID, login, name, "en", {"location": "Forest", "status": "Stay"}, [], 100, 0, 0,
                            {"cloths": "Rags", "weapon": "Stick"}, {}, {}, ["en", "ru"])
    account.update_data()
    return account


def create_exist_account(ID: int) -> player.Player:
    player_data = get_dict_from_json(f"../players_data/{ID}.json")
    return player.Player(player_data["ID"], player_data["login"], player_data["name"],
                         player_data["language"], player_data["location"], player_data["previous_locations"],
                         player_data["hp"], player_data["experience"], player_data["money"], player_data["equipment"],
                         player_data["inventory"], player_data["enemies"], player_data["buttons"])


def except_new_account(ID: int, login: str, name: str) -> player.Player:
    if f"{ID}.json" in os.listdir("../players_data/"):
        return create_exist_account(ID)
    return create_new_account(ID, login, name)


def execute_action(action: str, ID: int, login: str, name: str) -> str:
    account = except_new_account(ID, login, name)
    return account.perform_action(action)


def get_action_buttons(ID: int) -> list[str]:
    account = create_exist_account(ID)
    return account.buttons


def get_player_info(ID: int, login: str, name: str) -> str:
    account = except_new_account(ID, login, name)
    return account.info()


def get_player_inventory_info(ID: int, login: str, name: str) -> str:
    account = except_new_account(ID, login, name)
    return account.inventory_info()
