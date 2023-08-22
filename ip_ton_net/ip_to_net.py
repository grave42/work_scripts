import ipaddress
import csv

def cvs_maker(csv_filename):
    with open(csv_filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row[2] == "Cyfral":
                ip_list_cyfral.append(row[0])
                ip_list_cyfral.append(row[1])
            elif row[2] == "Ertelecom":
                ip_list_erth.append(row[0])
                ip_list_erth.append(row[1])
            else:
                ip_error.append(row)

def net_maker(ip_list):
    # Преобразуем IP-адреса в объекты ipaddress.IPv4Address
    ip_objects = [ipaddress.IPv4Address(ip) for ip in ip_list]
    # Группируем IP-адреса в подсети
    subnets = ipaddress.collapse_addresses(ip_objects)
    # Выводим найденные подсети
    return subnets



if __name__ == '__main__':
    ip_list_erth = []
    ip_list_cyfral = []
    ip_error = []
    cvs_maker("ip_pools_spb.csv")
    subnets_erth = []
    for i in net_maker(ip_list_erth):
        subnets_erth.append(i)
    subnets_cyfr = []
    for i in net_maker(ip_list_cyfral):
        subnets_cyfr.append(i)
    for i in subnets_cyfr:
        print(i)
    # net_maker()
    # Преобразуем IP-адреса в объекты ipaddress.IPv4Address
    # ip_objects = [ipaddress.IPv4Address(ip) for ip in ip_list]
    # # Группируем IP-адреса в подсети
    # subnets = ipaddress.collapse_addresses(ip_objects)
    # # Выводим найденные подсети
    # for subnet in subnets:
    #     print(subnet)