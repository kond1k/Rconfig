from device_command import exec_command
import re
import ipaddress

all_info_list = []
all_objects = {}


def get_info_from_csp(host, user, passwd):
    # Достает информацию
    answer = exec_command(host, user, passwd, command_to_device='sa_mgr show -isakmp -detail\n')
    print(answer)
    with open(f'info/certinfoisakmp{host}.txt', 'w') as f:
        #     f.write(answer.split('found.')[-1].strip())
        f.write(answer)


def get_device_cert(host, user, passwd):
    with open(f'info/certinfoisakmp{host}.txt') as f:
        iplist = f.read().strip().split("ISAKMP connection id:")
    all_info_list.append(iplist[1:])
    # with open(f'info/all_cert_info{host}.txt', 'a') as fc:
    #     for cert in f:
    #         index = cert.split(' ')[0]
    #         answer = exec_command(host, user, passwd,
    #                               command_to_device=f'cert_mgr show -i {index}\n')
    #         print(answer)
    #         fc.write(answer + '=' * 30)


# def get_cert_info_from_csp
#                 answer = exec_command('10.251.253.243', 'root', 'LmplhmTuhY5K3wKfVEXEOsfb',
#                                       command_to_device=f'cert_mgr show -i {index}\n')

if __name__ == '__main__':
    ip_list = ["10.254.253.242", "10.254.253.243", "10.253.253.242", "10.253.253.243", "10.252.253.242",
               "10.252.253.243", "10.251.253.242"]
    for ip in ip_list:
        get_device_cert(ip, 'root', 'LmplhmTuhY5K3wKfVEXEOsfb')
        # with open('allicmp.txt', 'a') as icmp:
    for ip in all_info_list:
        for device in ip:
            # ip = re.search('\d+', device.split('\n')[6])
            # cn = device.split('\n')[12]
            # print(ip, cn) \.+ (?P<ip>\d+.\d+.\d+.\d+)
            ip = re.search('remote .+ (?P<ip>\d+.\d+.\d+.\d+)', device)
            cn = re.search('remote identity \(DN\): .+CN=(?P<cn>.+)', device)
            if cn:
                all_objects[ipaddress.ip_address(ip['ip'])] = cn['cn']

    sortlist = list(all_objects.keys())
    sortipv4 = sorted([ipaddress.ip_address(i) for i in sortlist])
    # with open('allobjectsip.txt', 'w') as icmp:
    #     for ip in sortipv4:
    #         icmp.write(f'{ip} {all_objects[ip]}\n')
    all_ip_from_plan = {}
    with open('ip_from_plan.txt') as file:
        all_ip = file.read().split('\n')
    for ip in all_ip:
        ipv4 = ipaddress.ip_address(ip.split('\t')[1][0:-4] + '6')
        all_ip_from_plan[ipv4] = ip.split('\t')[0]
    sortipv4_from_plan = sorted([i for i in all_ip_from_plan.keys()])
    with open('ip_from_plan_unsight.txt', 'w') as unsight:
        for ip in all_ip_from_plan.keys():
            if ip not in all_objects.keys():
                unsight.write(f'{all_ip_from_plan[ip]}\n')
                # print(f'{ip} {all_ip_from_plan[ip]}')
    # get_info_from_csp(ip, 'root', 'LmplhmTuhY5K3wKfVEXEOsfb')
