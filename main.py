import paramiko
import logging
import time


def edit_ip():
    with open('files/ip_dds.txt') as f:
        iplist = list(filter(None, f.read().split('\n')))
        newiplist = []
        for ip in iplist:
            newiplist.append(ip.split('/')[0])
        with open('files/new_ip_dds.txt', 'w') as fw:
            for ip in newiplist:
                fw.write(ip.replace('10', '48', 1) + '\n')


def save_conf(hosts, user, secret, port):
    command = "save\nY\n"
    for host in hosts:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(hostname=host, password=secret,
                           username=user, port=port, allow_agent=False, look_for_keys=False)
            data = client.invoke_shell()
            time.sleep(1)
            # data.send(command)
            # time.sleep(10)
            answer = data.recv(10000).decode('utf-8')
            print(answer)
            with open(f'hosts/success/success.txt', 'a') as suc:
                suc.write(host + '\n')
            client.close()
        except paramiko.ssh_exception.NoValidConnectionsError:
            with open(f'hosts/fail/{host}.txt', 'w') as fail:
                fail.write('Не удалось подключиться')
        except TimeoutError:
            with open(f'hosts/fail/{host}c.txt', 'w') as fail:
                fail.write('Попытка установить соединение была безуспешной, т.к. от другого компьютера за требуемое '
                           'время не получен нужный отклик')
        except paramiko.ssh_exception.AuthenticationException:
            with open(f'hosts/fail/{host}a.txt', 'w') as fail:
                fail.write('Ошибка авторизации')
        except ConnectionResetError:
            with open(f'hosts/fail/{host}r.txt', 'w') as fail:
                fail.write('Хост разорвал соединение')


def add_user(hosts, user, secret, port):
    command = "system-view\naaa\nlocal-user rconfig password irreversible-cipher 5bWqIGe7rPIBMrq1kJkc privilege level " \
              "2\nlocal-user rconfig service-type telnet terminal ssh\ncommand-privilege level 2 view cli_8f display " \
              "current-configuration\ndisplay version\n"
    for host in hosts:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(hostname=host, password=secret,
                           username=user, port=port, allow_agent=False, look_for_keys=False)
            data = client.invoke_shell()
            time.sleep(1)
            data.send(command)
            time.sleep(20)
            answer = data.recv(10000).decode('utf-8')
            with open(f'hosts/success/{host}.txt', 'w') as suc:
                suc.write(answer)
            client.close()
        except paramiko.ssh_exception.NoValidConnectionsError:
            with open(f'hosts/fail/{host}.txt', 'w') as fail:
                fail.write('Не удалось подключиться')
        except TimeoutError:
            with open(f'hosts/fail/{host}c.txt', 'w') as fail:
                fail.write('Попытка установить соединение была безуспешной, т.к. от другого компьютера за требуемое '
                           'время не получен нужный отклик')
        except paramiko.ssh_exception.AuthenticationException:
            with open(f'hosts/fail/{host}a.txt', 'w') as fail:
                fail.write('Ошибка авторизации')


if __name__ == '__main__':
    with open('files/new_ip_dds.txt') as f:
        hosts = f.read().split('\n')
    # hosts = ['48.0.4.2']
    user = 'admin'
    secret = '1qazxsw2'
    port = 22
    # add_user(hosts, user, secret, port)
    # edit_ip()
    save_conf(hosts, user, secret, port)
