import requests
import json
import datetime
from tkinter import messagebox
import mysql.connector
import time
from ImageGenerator import generator


def execute_proccess(config: dict):
    date1: datetime = datetime.datetime.now()
    date = datetime.date(year=date1.year, month=date1.month, day=date1.day)

    result = execute_command(date, config)

    if result == 1:
        insert_database(date, config)
        generator(config)
        return 1
    else:
        return 0


def execute_command(date: datetime, config: dict):
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
        execute_proccess()

    if not response.status_code == 200:
        print(f'An exception has occurred with response status {response.status_code}, try again')
        time.sleep(1.5)
        execute_proccess()

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


def insert_database(init_date, config: dict):
    data = json.loads(open("data.json", "r").read())

    # You can use this structure to add any rate value you want to extract from the JSON and store in your database
    if data.get('tasas', {}).get('USD') is not None:
        insert_data((data['tasas']['USD']), 'USD', init_date, config)

    if data.get('tasas', {}).get('MLC') is not None:
        insert_data((data['tasas']['MLC']), 'MLC', init_date, config)

    if data.get('tasas', {}).get('ECU') is not None:
        insert_data((data['tasas']['ECU']), 'EUR', init_date, config)

    return 1


def insert_data(var, name: str, date: datetime, config: dict):
    cnx = mysql.connector.connect(user=(config['data']['user']), password=(config['data']['password']),
                                  host=(config['data']['host']), database=(config['data']['database']))

    cursor = cnx.cursor()

    query = f"INSERT INTO {config['data']['table']} (nombre, valor, fecha) VALUES (%s, %s, %s)"

    cursor.execute(query, (name, var, date))

    cnx.commit()

    cnx.close()
