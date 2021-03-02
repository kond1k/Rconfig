import paramiko
import time
import argparse
import random
import base64
import re
from pathlib import Path

CRYPT_ERROR = 'Ошибка криптографии'
CONNECT_ERROR = 'Ошибка подключения'
VERSION_ERROR = 'Не подходящий алгоритм шифрования, используйте другой скрипт'


def exec_command_get_cert(host, user, secret, commands, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host, password=secret,
                       username=user, port=port, allow_agent=False, look_for_keys=False)
        data = client.invoke_shell()
        time.sleep(2)
        for command in commands:
            data.send(f"{command}\n")
            time.sleep(2)
        answer = data.recv(100000).decode('utf-8')
        print(answer)
        with open('answers.txt', 'a') as f:
            f.write(answer + '\n')

    except paramiko.ssh_exception.NoValidConnectionsError:
        with open('fail_hosts.txt', 'a') as fail:
            fail.write(f'{host} Не удалось подключиться')
    except TimeoutError:
        with open('fail_hosts.txt', 'a') as fail:
            fail.write(
                f' {host} Попытка установить соединение была безуспешной, т.к. от другого компьютера за требуемое '
                'время не получен нужный отклик\n')
    except paramiko.ssh_exception.AuthenticationException:
        with open('fail_hosts.txt', 'a') as fail:
            fail.write(f'{host} Ошибка авторизации')
    except (IndexError, TypeError):
        with open('fail_hosts.txt', 'a') as fail:
            fail.write(f'{host} Ошибка индексации, повторите запрос\n')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ip host')
    parser.add_argument('-host', action="store", dest='host')
    parser.add_argument('-file', action="store_true", dest='file')
    host = parser.parse_args().host
    commands = []
    with open ('commands.txt') as f:
        for command in f:
            commands.append(command.strip())
    if parser.parse_args().file:
        with open('ip.txt') as iplist:
            for host in iplist:
                print(host)
                exec_command_get_cert(host.strip(), 'root', base64.b64decode('MTIzcXdlQVNE'), commands)
    else:
        if host is None:
            host = input('введите ип\n')
        exec_command_get_cert(host.strip(), 'root', base64.b64decode('MTIzcXdlQVNE'),commands)
