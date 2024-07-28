import json
from tkinter import messagebox
from Hour import Hour
import schedule
import time
from DatabaseSQLite import DB
from CallApi import execute_proccess


def task() -> None:
    execute_proccess(config, database)


def alert() -> None:
    messagebox.showwarning("Alert",
                           "The SCRIPT tasks are executed in 15 MIN, make sure you have a good internet connection")


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

    database: DB = DB()

    schedule.every().day.at(f"{workhour.decrement()}:45").do(alert)
    schedule.every().day.at(workhour.hour + ":00").do(task)

    while True:
        schedule.run_pending()
        time.sleep(1)
