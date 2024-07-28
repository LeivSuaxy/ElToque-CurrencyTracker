import requests
import json
import datetime
from tkinter import messagebox
import time
from DatabaseSQLite import DB
from ImageGenerator import generator


def execute_proccess(config: dict, database: DB) -> None:
    date1: datetime = datetime.datetime.now()
    date = datetime.date(year=date1.year, month=date1.month, day=date1.day)

    result = execute_command(date, config, database)

    if result == 1:
        insert_database(date, database)
        # Generate image is out for now
        # generator(config)
    else:
        messagebox.showerror('Error', 'There was a problem executing the script')


def execute_command(date: datetime, config: dict, database: DB):
    # URL de la API

    url = f"https://tasas.eltoque.com/v1/trmi?date_from={date}%2000%3A00%3A01&date_to={date}%2023%3A59%3A01"

    # Tu token de acceso
    token = config['config']['token']

    # Headers de la petición
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Realizar la petición GET
    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        print(f'An exception has occurred: {e.strerror}, try again')
        time.sleep(1.5)
        execute_proccess(config, database)

    if not response.status_code == 200:
        print(f'An exception has occurred with response status {response.status_code}, try again')
        time.sleep(1.5)
        execute_proccess(config, database)

    # Verify if the response is correct
    if response.status_code == 200:
        # Convert the response to JSON
        data = response.json()

        with open('data.json', 'w') as f:
            json.dump(data, f)

        print('Finished JSON')
        return 1
    else:
        messagebox.showerror("Error generating JSON", f"Could not connect to the API: {response.status_code}")
        return 0


def insert_database(init_date, database: DB) -> None:
    data = json.loads(open("data.json", "r").read())

    database.open_connection()

    if data.get('tasas', {}).get('USD') is not None:
        database.insert_data((data['tasas']['USD']), 'USD', init_date)

    if data.get('tasas', {}).get('MLC') is not None:
        database.insert_data((data['tasas']['MLC']), 'MLC', init_date)

    if data.get('tasas', {}).get('ECU') is not None:
        database.insert_data((data['tasas']['ECU']), 'EUR', init_date)

    database.close_connection()
