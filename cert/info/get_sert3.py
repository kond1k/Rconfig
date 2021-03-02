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
VERSION_ERROR = 'Не подходящий алгоритм шифрования, используйте другой скрипт'


def exec_command_get_cert(host, user, secret, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host, password=secret,
                       username=user, port=port, allow_agent=False, look_for_keys=False)
        data = client.invoke_shell()
        time.sleep(2)
        data.send(f"cert_mgr create -subj 'CN=$HOSTNAME,OU=S-Terra KP,O=State-Funded Institution Moscow oblast Center 112,ST=Moscow oblast,C=RU ' -GOST_R3410EL\n")
        time.sleep(2)
        press = data.recv(100000).decode('utf-8')
        hostname = re.search(r'root@(\w+.\w+.\w+(-\w+)?)',press)
        if 'interpret the token' in press:
            print(VERSION_ERROR)
            cert_create_status[host] = VERSION_ERROR
            with open('fail_sert.txt', 'a') as f:
                f.write(f'{host} {VERSION_ERROR} \n')
            return 1
        if 'Crypto error. Unable to create certificate request' in press:
            print(CRYPT_ERROR)
            cert_create_status[host] = CRYPT_ERROR
            with open('fail_sert.txt', 'a') as f:
                f.write(f'{host} {CRYPT_ERROR} \n')
            return 1
        while "Press key" in press:
            print(press)
            sleep = random.randint(1, 4)
            prompt = press.split("key:")[-1].strip()
            print(prompt)
            data.send(prompt)
            time.sleep(sleep)
            press = data.recv(100000).decode('utf-8')
        answer = re.search(r'(?P<cert>-----.*-----)', press, flags = re.DOTALL)
        Path("hosts_certs").mkdir(parents=True, exist_ok=True)
        cert_create_status[host] = "SUCCESS"
        with open(f'hosts_certs/{host.strip()} {hostname.group(1)}.req', 'w') as f:
            f.write(answer['cert'])
            print(f"Complete {host}")

    except paramiko.ssh_exception.NoValidConnectionsError:
        with open('fail_sert.txt', 'a') as fail:
            fail.write(f'{host} Не удалось подключиться к CSP')
    except TimeoutError:
        with open('fail_sert.txt', 'a') as fail:
            fail.write(
                f' {host} Попытка установить соединение была безуспешной, т.к. от другого компьютера за требуемое '
                'время не получен нужный отклик')
    except paramiko.ssh_exception.AuthenticationException:
        with open('fail_sert.txt', 'a') as fail:
            fail.write(f'{host} Ошибка авторизации')
    except IndexError:
        cert_create_status[host] = 'Ошибка индексации'
        with open('fail_sert.txt', 'a') as fail:
            fail.write(f'{host} Ошибка индексации, повторите запрос\n')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ip host')
    parser.add_argument('-host', action="store", dest='host')
    parser.add_argument('-file', action="store_true", dest='file')
    host = parser.parse_args().host
    if parser.parse_args().file:
        with open('ip.txt') as iplist:
            for host in iplist:
                print(host)
                exec_command_get_cert(host.strip(), 'root', base64.b64decode('MTIzcXdlQVNE'))
            for key, value in cert_create_status.items():
                print(f'{key} {value}')
    else:
        if host is None:
            host = input('введите ип\n')
        exec_command_get_cert(host.strip(), 'root', base64.b64decode('MTIzcXdlQVNE'))
