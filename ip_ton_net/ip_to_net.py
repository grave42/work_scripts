import ipaddress
import socket
import struct
import csv


cyfr_prod = {
    '10.125.160.0/20': 10,
    '10.125.176.0/21': 5,
    '10.125.184.0/23': 5,
    '10.125.186.0/24': 5,
    '10.154.212.0/23': 5,
    '10.154.112.0/22': 5,
    '10.80.216.0/24': 5,
    '10.125.128.0/20': 5,
    '10.154.120.0/21': 5,
    '10.80.217.0/24': 5,
    '10.80.215.0/24': 5,
    '10.154.104.0/21': 5,
    '10.125.187.0/24': 2,
    '10.125.188.0/22': 2,
    '10.81.0.0/19': 7,
    '10.81.64.0/18': 7
}


erth_prod = {
    '10.80.0.0/17': 2,
    '10.80.128.0/18': 2,
    '10.125.0.0/18': 2,
    '10.166.254.0/24': 8,
    '10.80.224.0/19': 9 #(НЕ УДАЛЯЕМ ИЗ БД)
}

def ip_range(start_ip, end_ip):
    try:
        start = struct.unpack('>I', socket.inet_aton(start_ip))[0]
        end = struct.unpack('>I', socket.inet_aton(end_ip))[0]
        return [socket.inet_ntoa(struct.pack('>I', i)) for i in range(start, end + 1)]
    except socket.error:
        print("Invalid IP address format")
        return None



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

def cvs_db_request_maker(sub_list, company):
    with open(f'DB_REQ_list_{company}.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for subnet in sub_list:
            if company == 'cyfral':
                for key, value in cyfr_prod.items():
                    if subnet.subnet_of(ipaddress.ip_network(key)):
                        cgi = value
                        break
                    else:
                        cgi = 5
            sel = f'''insert into networks (net, city_id, company_id, conf_group_id) values ('{subnet}', 27, 2, {cgi});'''
            csvwriter.writerow([sel])





if __name__ == '__main__':
    ip_list = []
    subs_list = []
    filename = 'result_erth.csv'
    cvs_maker2(filename)
    subs = net_maker(ip_list)
    with open(f'SUBNET_list_{filename}', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for i in subs:
            csvwriter.writerow([str(i)])
            subs_list.append(i)
        print("Кол-во подсетей: " + str(len(subs_list)))
    # cvs_db_request_maker(subs_list, 'cyfral')
    # net_maker()
    # Преобразуем IP-адреса в объекты ipaddress.IPv4Address
    # ip_objects = [ipaddress.IPv4Address(ip) for ip in ip_list]
    # # Группируем IP-адреса в подсети
    # subnets = ipaddress.collapse_addresses(ip_objects)
    # # Выводим найденные подсети
    # for subnet in subnets:
    #     print(subnet)