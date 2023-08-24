import csv

def ip_to_tuple(ip):
    return tuple(map(int, ip.split('.')))

# Чтение CSV файла и создание списка записей
input_file = 'all_dia.csv'
output_file = 'sorted_output.csv'

ip_ranges = []

with open(input_file, 'r', encoding='cp1251') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=';')
    for row in csv_reader:
        ip_start = row['ip_start']
        ip_stop = row['ip_stop']
        company = row['company']
        ip_ranges.append({'ip_start': ip_start, 'ip_stop': ip_stop, 'company': company})

# Сортировка списка диапазонов IP по 4-м октетам начального IP
sorted_ip_ranges = sorted(ip_ranges, key=lambda x: ip_to_tuple(x['ip_start']))

# Запись отсортированных данных обратно в CSV файл
with open(output_file, 'w', newline='', encoding='cp1251') as csv_file:
    fieldnames = ['ip_start', 'ip_stop', 'company']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
    csv_writer.writeheader()
    csv_writer.writerows(sorted_ip_ranges)

print("Сортировка завершена. Результат записан в", output_file)