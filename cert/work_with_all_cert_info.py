import datetime
import time
import re

if __name__ == '__main__':
    certs = {}
    host = '10.251.253.243'
    with open(f'info/all_cert_info{host}.txt') as f:
        all_cert = f.read().strip().split('=' * 30)
        i = 1
        for cert in all_cert:
            # re.search('(?P<mac>\S+) +(?P<ip>\S+) +\d+ +\S+ +(?P<vlan>\d+) +(?P<port>\S+)', line)
            match = re.search('(?P<cn>CN=\S+)', cert)
            matchd = re.search('(Valid to:) +(?P<date>\w{3} \w{3}\s+\d+ \d+:\d+:\d+ \d+)', cert)
            if matchd:
                print(match.group('cn'))
                print(matchd.group('date'))
                print(i)
                i += 1
    #         for line in cert.split('\n'):
    #             if 'Subject' in line:
    #                 name = line.split('CN=')[-1]
    #             if 'Valid to' in line:
    #                 exp_date = time.strptime(line.split('to:')[-1].strip())
    #             if line != '':
    #                 print(line)
    #                 # print(name)
    #         certs[name] = exp_date
    #         print('\n')
    # with open('info/cert_valid.txt', 'w') as valid:
    #     list_c = list(certs.items())
    #     list_c.sort(key=lambda i: i[1])
    #     for cs in list_c:
    #         valid.write(f'{cs[0]:<20} ' + time.strftime('%B %d %Y', cs[1]) + '\n')
