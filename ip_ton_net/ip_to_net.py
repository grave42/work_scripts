import ipaddress
import socket
import struct
import csv

def ip_range(start_ip, end_ip):
    start = struct.unpack('>I', socket.inet_aton(start_ip))[0]
    end = struct.unpack('>I', socket.inet_aton(end_ip))[0]

    return [socket.inet_ntoa(struct.pack('>I', i)) for i in range(start, end + 1)]


def cvs_maker2(filename):
    f = open(filename, 'r')
    csvreader = csv.reader(f, delimiter=';')

    for row in csvreader:
        start_ip = row[0]
        end_ip = row[1]
        ip_range2 = ip_range(start_ip, end_ip)
        for ip in ip_range2:
            ip_list.append(ip)


def net_maker(ip_list):
    # Преобразуем IP-адреса в объекты ipaddress.IPv4Address
    ip_objects = [ipaddress.IPv4Address(ip) for ip in ip_list]
    # Группируем IP-адреса в подсети
    subnets = ipaddress.collapse_addresses(ip_objects)
    # Выводим найденные подсети
    return subnets

# def cvs_db_request_maker(sub_list):
#     with open('DB_RE)




if __name__ == '__main__':
    ip_list = []
    subs_list = []
    filename = 'erth_spb.csv'
    cvs_maker2(filename)
    subs = net_maker(ip_list)
    with open(f'SUBNET_list_{filename}', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for i in subs:
            csvwriter.writerow([str(i), '47QUv7J6bR'])
            subs_list.append(i)
        print(len(subs_list))

    # net_maker()
    # Преобразуем IP-адреса в объекты ipaddress.IPv4Address
    # ip_objects = [ipaddress.IPv4Address(ip) for ip in ip_list]
    # # Группируем IP-адреса в подсети
    # subnets = ipaddress.collapse_addresses(ip_objects)
    # # Выводим найденные подсети
    # for subnet in subnets:
    #     print(subnet)