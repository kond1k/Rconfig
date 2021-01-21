import datetime
import time

if __name__ == '__main__':
    certs = {}
    with open('info/all_cert_info.txt') as f:
        all_cert = f.read().split('=' * 30)
        for cert in all_cert:
            for line in cert.split('\n'):
                if 'Subject' in line:
                    name = line.split('CN=')[-1]
                if 'Valid to' in line:
                    exp_date = time.strptime(line.split('to:')[-1].strip())
                if line != '':
                    print(line)
                    # print(name)
            certs[name] = exp_date
            print('\n')
    with open('info/cert_valid.txt', 'w') as valid:
        list_c = list(certs.items())
        list_c.sort(key=lambda i: i[1])
        # mont = value.split('  ')[-2].split(' ')[-1]
        # day = value.split('  ')[-1].split(' ')[0]
        # year = value.split('  ')[-1].split(' ')[-1]
        # date = f'{mont} {day} {year}'
        for cs in list_c:
            valid.write(f'{cs[0]:<20} ' + time.strftime('%B %d %Y', cs[1]) + '\n')
