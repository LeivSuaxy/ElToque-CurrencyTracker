import mysql.connector
import os
import matplotlib.pyplot as plt


def get_values(name, config: dict) -> list:
    cnx = mysql.connector.connect(user=(config['data']['user']), password=(config['data']['password']),
                                  host=(config['data']['host']), database=(config['data']['database']))

    cursor = cnx.cursor()

    query = f"SELECT {config['rows']['value']} FROM {config['data']['table']} WHERE {config['rows']['name']}='{name}'"

    cursor.execute(query)

    value_list: list = []

    for (valor,) in cursor:
        value_list.append(valor)

    cursor.close()
    cnx.close()

    return value_list


def get_date(name, config: dict) -> list:
    date_list: list = []

    cnx = mysql.connector.connect(user=(config['data']['user']), password=(config['data']['password']),
                                  host=(config['data']['host']), database=(config['data']['database']))

    cursor = cnx.cursor()

    query = f"SELECT {config['rows']['date']} FROM {config['data']['table']} WHERE {config['rows']['name']}='{name}'"

    cursor.execute(query)

    for (date,) in cursor:
        date_list.append(date)

    cursor.close()
    cnx.close()

    return date_list


def generate_images(date_list, value_list, name) -> None:
    plt.figure(figsize=(20, 20))
    plt.plot(date_list, value_list, '-')

    desktop_route = os.path.join(os.path.expanduser("~"), "Desktop")

    width_inches = 1920 / 80
    height_inches = 1080 / 80
    plt.gcf().set_size_inches(width_inches, height_inches)

    plt.title(f'Variation of {name} in 2024')

    plt.xlabel('Days in 2024')
    plt.ylabel(f'Value of {name}')

    plt.savefig(os.path.join(desktop_route, f'Variation of {name} in 2024'), dpi=300)


def generator(config: dict) -> None:
    list_names = {'USD', 'MLC', 'EUR'}

    for name in list_names:
        lista_dates = get_date(name, config)
        lista_values = get_values(name, config)
        generate_images(lista_dates, lista_values, name)
