import os


def clear_logs():
    with open(f"{os.getcwd()}/orders/history.log", "w") as file:
        file.write("")
