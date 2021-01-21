from device_command import exec_command


def get_info_from_csp(host, user, passwd):
    # Достает информацию
    answer = exec_command(host, user, passwd, command_to_device='cert_mgr show\n')
    with open('info/certinfo.txt', 'a') as f:
        #     f.write(answer.split('found.')[-1].strip())
        for line in answer.split('found.')[-1].strip().split('\n'):
            if 'CN' in line:
                f.write(line)


def get_device_cert(host, user, passwd):
    with open('info/certinfo.txt') as f:
        with open('info/all_cert_info.txt', 'a') as fc:
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
