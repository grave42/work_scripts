import csv
import logging
import requests

# Создание собственного логгера с желаемым именем
logger = logging.getLogger("my_logger")
# Настройка уровня логирования
logger.setLevel(logging.INFO)

# Создание обработчика
file_handler = logging.FileHandler("logfile.log")
formatter = logging.Formatter('%(message)s')  # Установка формата сообщения
file_handler.setFormatter(formatter)
# Добавление обработчика к логгеру
logger.addHandler(file_handler)

def get_pass(_ip):
    try:
        pass_list = ['GnaiHy', 'GnaiHy9155', 'user1']
        for pas in pass_list:
            r = requests.get('http://{}/cgi-bin/images_cgi'.format(_ip), auth=('user1', '{}'.format(pas)),
                             timeout=5)
            if r.status_code == 200:
                logger.info(f"{_ip};{pas}")
                return pas
                break
        logger.warning(f"{_ip};WRONG PASSWORD")
    except Exception as ex:
        logger.warning(f"{_ip};DEVICE DOWN")
        print(ex)


if __name__ == '__main__':
    f = open('wrong_auth_user1.csv', 'r')
    csvreader = csv.reader(f, delimiter=';')
    for row in csvreader:
        print("Работаю с " + row[0])
        get_pass(row[0])
    print("*** FINISH ***")
