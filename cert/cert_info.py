from device_command import exec_command


def get_info_from_csp(host, user, passwd):
    # Достает информацию
    answer = exec_command(host, user, passwd, command_to_device='cert_mgr show\n')
    with open(f'info/certinfo{host}.txt', 'a') as f:
        #     f.write(answer.split('found.')[-1].strip())
        for line in answer.split('found.')[-1].strip().split('\n'):
            if 'CN' in line:
                f.write(line)


def get_device_cert(host, user, passwd):
    with open(f'info/certinfo{host}.txt') as f:
        with open(f'info/all_cert_info{host}.txt', 'a') as fc:
            for cert in f:
                index = cert.split(' ')[0]
                answer = exec_command(host, user, passwd,
                                      command_to_device=f'cert_mgr show -i {index}\n')
                print(answer)
                fc.write(answer + '=' * 30)


# def get_cert_info_from_csp
#                 answer = exec_command('10.251.253.243', 'root', 'LmplhmTuhY5K3wKfVEXEOsfb',
#                                       command_to_device=f'cert_mgr show -i {index}\n')

if __name__ == '__main__':
    ip_list = ["10.254.253.242", "10.254.253.243", "10.253.253.242", "10.253.253.243", "10.252.253.242",
               "10.252.253.243", "10.251.253.242"]
    for ip in ip_list:
        get_info_from_csp(ip, 'root', 'LmplhmTuhY5K3wKfVEXEOsfb')
        get_device_cert(ip, 'root', 'LmplhmTuhY5K3wKfVEXEOsfb')
