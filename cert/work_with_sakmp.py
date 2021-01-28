import re
import ipaddress

if __name__ == '__main__':
    # all_ip_from_plan = {}
    # with open('ip_from_plan.txt') as file:
    #     all_ip = file.read().split('\n')
    # for ip in all_ip:
    #     ipv4 = ipaddress.ip_address(ip.split('\t')[1][0:-4] + '6')
    #     all_ip_from_plan[ipv4] = ip.split('\t')[0]
    # sortipv4 = sorted([i for i in all_ip_from_plan.keys()])
    # with open('ip_from_plan_sotred.txt', 'w') as sorted:
    #     for ip in sortipv4:
    #         sorted.write(f'{ip} {all_ip_from_plan[ip]}\n')
    all_cs = set()
    with open('ip_from_certcentr.txt') as f:
        a = f.read().split('\n')
    for dev in a:
        if 'cs' in dev:
            all_cs.add(dev)
    with open('name_from_certcentr.txt', 'w') as f:
        for cs in all_cs:
            f.write(f'{cs}\n')
    print(all_cs)
