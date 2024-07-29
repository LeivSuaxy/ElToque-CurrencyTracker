import datetime
import requests
import time
from Tools.DatabaseSQLite import DB
import json
from tkinter import messagebox


def call_api():
    try:
        res = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        print(f'An exception has occurred: {e.strerror}, try again')
        time.sleep(1.5)
        res = call_api()

    return res


def insert_database() -> None:
    response_data = json.loads(open("data.json", "r").read())

    database.open_connection()

    if response_data.get('tasas', {}).get('USD') is not None:
        database.insert_data((response_data['tasas']['USD']), 'USD', date)

    if response_data.get('tasas', {}).get('MLC') is not None:
        database.insert_data((response_data['tasas']['MLC']), 'MLC', date)

    if response_data.get('tasas', {}).get('ECU') is not None:
        database.insert_data((response_data['tasas']['ECU']), 'EUR', date)


if __name__ == '__main__':
    config = json.loads(open('config.json', 'r').read())
    database: DB = DB()
    token = config['config']['token']
    date = datetime.date.today()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    url = f"https://tasas.eltoque.com/v1/trmi?date_from={date}%2000%3A00%3A01&date_to={date}%2023%3A59%3A01"

    status_ok = False

    while status_ok is False:
        database.open_connection()
        response = call_api()

        if response.status_code == 200:
            data = response.json()

            with open('data.json', 'w') as f:
                json.dump(data, f)

            insert_database()
            database.close_connection()
            status_ok = True
        elif response.status_code == 429:
            print('Ups! Demasiado Rapido, Try Again...')
            database.close_connection()
        elif response.status_code == 400:
            print('HTTP_400_BAD_REQUEST')
            print('Maybe day out of data')
            database.close_connection()
        elif response.status_code == 422:
            print('Missing token')
            print(response.status_code)
            database.close_connection()
            break
        else:
            messagebox.showerror("Error generating JSON", f"Could not connect to the API: {response.status_code}")
            break

        time.sleep(2.0)

    print('Finalizado!')
