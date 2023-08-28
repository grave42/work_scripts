import ipaddress
import pandas as pd

# Чтение CSV файла
data = pd.read_csv('sorted_output.csv', delimiter=';')

# Преобразование строковых IP-адресов в объекты ipaddress.IPv4Address
data['ip_start'] = data['ip_start'].apply(ipaddress.IPv4Address)
data['ip_stop'] = data['ip_stop'].apply(ipaddress.IPv4Address)

# Сортировка данных по начальному IP-адресу
data = data.sort_values(by='ip_start')

# Создание списка диапазонов
ranges = []
prev_range = None

for _, row in data.iterrows():
    if prev_range is None:
        prev_range = (row['ip_start'], row['ip_stop'])
    else:
        if row['ip_start'] > prev_range[1] + 1:
            ranges.append((prev_range[1] + 1, row['ip_start'] - 1))
        prev_range = (row['ip_start'], max(row['ip_stop'], prev_range[1]))

# Добавление первого недостающего диапазона, если начальный адрес не 10.80.0.0
if ranges and ranges[0][0] > ipaddress.IPv4Address('10.125.0.1'):
    ranges.insert(0, (ipaddress.IPv4Address('10.125.0.1'), ranges[0][0] - 1))

# Добавление последнего недостающего диапазона, если конечный адрес не 10.80.127.255
if ranges and ranges[-1][1] < ipaddress.IPv4Address('10.125.255.254'):
    ranges.append((ranges[-1][1] + 1, ipaddress.IPv4Address('10.125.255.254')))

# Вывод результата
for start, stop in ranges:
    print(f"{start};{stop};NewRangeCompany")