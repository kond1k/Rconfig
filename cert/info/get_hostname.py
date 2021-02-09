import paramiko
import time
import argparse
import random
import base64
import re
from pathlib import Path

cert_valid_dict = {}
cert_create_status = {}  # конечный статус операции
CRYPT_ERROR = 'Ошибка криптографии'
CONNECT_ERROR = 'Ошибка подключения'


def exec_command_get_cert(host, user, secret, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host, password=secret,
                       username=user, port=port, allow_agent=False, look_for_keys=False)
        data = client.invoke_shell()
        time.sleep(2)
        version = data.recv(100000).decode('utf-8')
        hostname = re.search(r'root@(\w+.\w+.\w+(-\w+)?)',version)
        print(hostname.group(1))
        with open('devices_info_hostname.txt', 'a') as f:
            f.write(f"{hostname.group(1)}\n")


    except paramiko.ssh_exception.NoValidConnectionsError:
        with open('fail.txt', 'a') as fail:
            fail.write(f'{host} Не удалось подключиться к хосту\n')
    except TimeoutError:
        with open('fail.txt', 'a') as fail:
            fail.write(
                f' {host} Попытка установить соединение была безуспешной, т.к. от другого компьютера за требуемое '
                'время не получен отклик\n')
    except paramiko.ssh_exception.AuthenticationException:
        with open('fail.txt', 'a') as fail:
            fail.write(f'{host} Ошибка авторизации\n')
    except IndexError:
        cert_create_status[host] = 'Ошибка индексации'
        with open('fail.txt', 'a') as fail:
            fail.write(f'{host} Ошибка индексации, повторите запрос\n')
    except EOFError:
        with open('fail.txt', 'a') as fail:
            fail.write(f'{host} Соединение разорвано хостом\n')
    except TypeError:
        with open('fail.txt', 'a') as fail:
            fail.write(f'{host} Ошибка индексации, повторите запрос\n')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ip host')
    parser.add_argument('-host', action="store", dest='host')
    parser.add_argument('--file', action="store_true", dest='file')
    host = parser.parse_args().host
    if parser.parse_args().file:
        with open('ip.txt') as iplist:
            for ip in iplist:
                print(ip, end='')
                exec_command_get_cert(ip.strip(), 'root', base64.b64decode('MTIzcXdlQVNE'))
            # for key, value in cert_create_status.items():
            #     print(f'{key} {value}')
    else:
        if host is None:
            host = input('введите ип\n')
            # host = '10.17.4.36'
        exec_command_get_cert(host, 'root', base64.b64decode('MTIzcXdlQVNE'))
