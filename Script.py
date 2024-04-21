import json
from tkinter import messagebox
from Hour import Hour
import schedule
import time
from CallApi import execute_proccess


def task():
    execute_proccess(config)


def alert():
    messagebox.showwarning("Alert",
                           "The SCRIPT tasks are executed in 15 MIN, make sure you have a good internet connection")


def check_config_database(config: dict) -> bool:
    if config.get('data', {}).get('user') is None:
        return False

    if config.get('data', {}).get('password') is None:
        return False

    if config.get('data', {}).get('host') is None:
        return False

    if config.get('data', {}).get('database') is None:
        return False

    return True


if __name__ == '__main__':
    config = json.loads(open("config.json", "r").read())
    workhour: Hour

    if config.get('config', {}).get('token') is None:
        messagebox.showerror('Error', 'Token is Empty, please enter your token in config.json')

    if config.get('config', {}).get('hour') is None:
        print('Hour is not defined')
        # Predefined Hour
        workhour = Hour(20, 0)
    else:
        workhour = Hour((config['config']['hour']), 0)

    if not check_config_database(config):
        messagebox.showerror('Error', 'Error, complete the database information')

    schedule.every().day.at(f"{workhour.decrement()}:45").do(alert)
    schedule.every().day.at(workhour.hour + ":00").do(task)

    while True:
        schedule.run_pending()
        time.sleep(1)
