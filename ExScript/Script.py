import datetime
import requests
import time
from Tools.DatabaseSQLite import DB
import json
import calendar
from tkinter import messagebox


def call_api():
    try:
        res = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        print(f'An exception has occurred: {e.strerror}, try again')
        time.sleep(1.5)
        res = call_api()

    return res


def increment_date():
    # Incrementar la fecha en un día
    next_day = date + datetime.timedelta(days=1)

    # Verificar si el día es mayor que el número de días en el mes actual
    last_day_of_month = calendar.monthrange(next_day.year, next_day.month)[1]
    if next_day.day > last_day_of_month:
        # Incrementar el mes
        if next_day.month == 12:
            next_day = datetime.date(next_day.year + 1, 1, 1)
        else:
            next_day = datetime.date(next_day.year, next_day.month + 1, 1)

    return next_day


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
    date = datetime.date(2021, 1, 1)
    database: DB = DB()
    token = config['config']['token']

    headers = {
        "Authorization": f"Bearer {token}"
    }

    url = f"https://tasas.eltoque.com/v1/trmi?date_from={date}%2000%3A00%3A01&date_to={date}%2023%3A59%3A01"
    current_date = datetime.date.today()
    while date <= current_date:
        database.open_connection()
        response = call_api()

        if response.status_code == 200:
            print('HTTP_200_CODE OK!')
            # Convert the response to JSON
            data = response.json()

            with open('data.json', 'w') as f:
                json.dump(data, f)

            print('Finished JSON')

            insert_database()
            date = increment_date()
            url = f"https://tasas.eltoque.com/v1/trmi?date_from={date}%2000%3A00%3A01&date_to={date}%2023%3A59%3A01"
            database.close_connection()
        elif response.status_code == 429:
            print('Ups! Demasiado Rapido, Try Again...')
            database.close_connection()
        elif response.status_code == 400:
            print('HTTP_400_BAD_REQUEST')
            print('Maybe day out of data')
            date = increment_date()
            url = f"https://tasas.eltoque.com/v1/trmi?date_from={date}%2000%3A00%3A01&date_to={date}%2023%3A59%3A01"
            database.close_connection()
        else:
            messagebox.showerror("Error generating JSON", f"Could not connect to the API: {response.status_code}")
            break

        time.sleep(2.0)

    print('Finalizado')
