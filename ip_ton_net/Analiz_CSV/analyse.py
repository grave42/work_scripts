import csv
import ipaddress
import asyncio
import psycopg2
import requests


class MH:
    db_params = {
        'dbname': 'myhomedb',
        'user': 'access_control_accounts_script',
        'password': 'Xt14bfCmdqJjTY9q',
        'host': 'c-c9qm9s495fchnmfvs59f.rw.mdb.yandexcloud.net',
        'port': '6432'
    }

    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()


def csv_reader_func(csv_file_path):
    delimiter = ';'
    list = []
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delimiter)
        for row in csv_reader:
            list.append(row)
    return list


def ip_in_cyfral(list_ip, list_ip_cyfral):
    mod_list_ip = []
    for ip in list_ip:
        mod_list_ip.append(ip[0])
    mod_list_ip_cyfr = []
    for i in list_ip_cyfral:
        mod_list_ip_cyfr.append(i[0])
    count = 0
    for ip in list_ip:
        if ip[0] in mod_list_ip_cyfr:
            ip[3] = "cyfral"
            count += 1
        else:
            continue
    print("Изменено с пометкой Cyfral: " + str(count))
    return list_ip


def ip_plus_cyfral(list_ip, list_ip_cyfral):
    mod_list_ip = []
    for ip in list_ip:
        mod_list_ip.append(ip[0])
    mod_list_ip_cyfr = []
    for i in list_ip_cyfral:
        mod_list_ip_cyfr.append(i[0])
    ip_addresses_found = [ip for ip in mod_list_ip_cyfr if ip not in mod_list_ip]
    for ip in ip_addresses_found:
        all_domofon.append([ip, "", "", "Cyfral", ""])


async def execute_query(ip):
    connection = psycopg2.connect(database="myhomedb",
                                  user="access_control_accounts_script",
                                  password="Xt14bfCmdqJjTY9q",
                                  host="c-c9qm9s495fchnmfvs59f.rw.mdb.yandexcloud.net",
                                  port="6432")
    cursor = connection.cursor()
    query = f"select accounts from access_control ac where ip_address = '{ip}' and is_removed is false"
    try:
        cursor.execute(query)
        pwd = cursor.fetchone()[0]['api']['password']
        cursor.close()
        connection.close()
        print('Cделал запрос:' + ip)
        return pwd
    except TypeError:
        print('Cделал запрос:' + ip)
        return None


async def myhome_check(list_ip):
    for ip in list_ip[1:]:
        pwd = await execute_query(ip[0])
        if pwd == '47QUv7J6bR':
            ip[2] = 'Ertelecom'
        elif pwd == 'Ldjhtwrbq24#':
            ip[2] = 'Ertelecom_spb'
        elif pwd == 'Cygr21Bw':
            ip[2] = 'Cyfral'
        elif pwd == 'admin':
            ip[2] = 'ADMIN'
        else:
            ip[2] = 'UNKNOWN'
    return list_ip

async def check_bruce(list_ip, list_bruce):
    for ip in list_ip[1:]:
        for dia in list_bruce:
            start_ip = ipaddress.IPv4Address(dia[0])
            end_ip = ipaddress.IPv4Address(dia[1])
            if start_ip <= ipaddress.IPv4Address(ip[0]) <= end_ip:
                ip[1] = dia[2]
                break
            else:
                ip[1] = 'UNKNOWN'
    return list_ip

def get_pass(list_ip):
    for ip in list_ip[1:]:
        print("Брутаю: " + str(ip[0]))
        try:
            pass_list = ['47QUv7J6bR', 'Ldjhtwrbq24#', 'Cygr21Bw', 'admin', 'mmkgobu']
            for pas in pass_list:
                r = requests.get('http://{}/cgi-bin/intercom_cgi?action=get'.format(ip[0]), auth=('admin', '{}'.format(pas)),
                                 timeout=10)
                if r.status_code == 200:
                    if pas == '47QUv7J6bR':
                        ip[4] = 'Ertelecom'
                    elif pas == 'Ldjhtwrbq24#':
                        ip[4] = 'Ertelecom_spb'
                    elif pas == 'Cygr21Bw':
                        ip[4] = 'Cyfral'
                    elif pas == 'admin':
                        ip[4] = 'ADMIN'
                    else:
                        ip[4] = 'UNKNOWN'
                    break
        except Exception:
            ip[4] = 'DEVICE DOWN'
    return list_ip




if __name__ == '__main__':
    all_domofon = csv_reader_func('all_domofon.csv')
    mhdb = MH()
    # rias = csv_reader_func('rias.csv')
    cyfral = csv_reader_func('cyfral.csv')
    bruce = csv_reader_func('bruce.csv')
    print("Домофонов из мониторинга: " + str(len(all_domofon)))
    all_domofon = ip_in_cyfral(all_domofon, cyfral)
    # Cклеиваем IP Сереги + Цифральские
    ip_plus_cyfral(all_domofon, cyfral)
    print("Домофоны из мониторинга + Цифральские: " + str(len(all_domofon)))
    # Проверка в myhome
    all_domofon = asyncio.run(myhome_check(all_domofon))
    print("Проверил в базе myhome: " + str(len(all_domofon)))
    # Проверка в брюсе
    all_domofon = asyncio.run(check_bruce(all_domofon, bruce))
    print("Проверил в Bruce")
    all_domofon = get_pass(all_domofon)
    print("Брутанул")
    with open('RESULT.csv', 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        for row in all_domofon:
            csv_writer.writerow(row)
    print("*** FINISH ***")

    ################################
