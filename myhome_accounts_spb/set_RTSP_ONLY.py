import json

import psycopg2
from psycopg2 import sql

# Замените значения на ваши параметры подключения
# db_params = {
#     'dbname': 'myhomedb',
#     'user': 'myhomedb',
#     'password': ':Mv2G62-N}?-5gQC',
#     'host': 'c-c9qrkch5hcj4s5dqao04.rw.mdb.yandexcloud.net',
#     'port': '6432'
# }

db_params = {
    'dbname': 'myhomedb',
    'user': 'access_control_accounts_script',
    'password': 'Xt14bfCmdqJjTY9q',
    'host': 'c-c9qm9s495fchnmfvs59f.rw.mdb.yandexcloud.net',
    'port': '6432'
}

# SQL-запрос для обновления значений
update_query = sql.SQL("""
    UPDATE access_control
    SET accounts = jsonb_set(accounts, %s, %s)
    WHERE ip_address = %s
""")

try:
    # Подключение к базе данных
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    # Значения для обновления
    path_rtsp_password = ['rtsp', 'password']
    new_password = 'GnaiHy9155'

    # Выполнение запроса

    with open('logfile.log', 'r') as log:
        for line in log:
            ip_pass = line.strip().split(';')
            cursor.execute(
                update_query,
                (path_rtsp_password, json.dumps(new_password), ip_pass[0])
            )
            print("Поменял для " + ip_pass[0])
            connection.commit()

    # Применение изменений
    connection.commit()

except (Exception, psycopg2.DatabaseError) as error:
    print("Error:", error)

finally:
    if connection:
        connection.close()
        print("*** FINISH ***")
