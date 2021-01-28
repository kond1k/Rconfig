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


def exec_command_get_cert(host, user, secret, port=22, host_ip='', action='get'):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host, password=secret,
                       username=user, port=port, allow_agent=False, look_for_keys=False)
        data = client.invoke_shell()
        time.sleep(2)
        data.send(f"ssh {host_ip}\n")
        time.sleep(5)
        data.send("yes\n")
        time.sleep(5)
        data.send(base64.b64decode('MTIzcXdlQVNE'))
        data.send('\n')
        time.sleep(2)
        data.send("cert_mgr show\n")
        time.sleep(2)
        local = data.recv(100000).decode('utf-8')
        if 'local' not in local:
            print(f'{CONNECT_ERROR} {host_ip}')
            cert_create_status[host_ip] = CONNECT_ERROR
            with open('fail.txt', 'a') as f:
                f.write(f'{host_ip} {CONNECT_ERROR} \n')
                return CONNECT_ERROR
        for cert in local.split('\n'):
            if 'local' in cert:
                answer = cert
                index = answer.split(' ')[0]
                obj = answer.split('local')[-1].strip()
                break
        time.sleep(2)
        if action == 'get':
            cert_request = create_request(data, obj, host_ip)
            Path("hosts").mkdir(parents=True, exist_ok=True)
            if 'Ошибка' in cert_request:
                cert_create_status[host_ip] = CRYPT_ERROR
            else:
                cert_create_status[host_ip] = "SUCCESS"
            with open(f'hosts\{host_ip.strip()}.txt', 'w') as f:
                f.write(cert_request)
                print(f"Complete {host_ip}")
        if action == 'info':
            get_cert_info(data, index)

    except paramiko.ssh_exception.NoValidConnectionsError:
        with open('fail.txt', 'a') as fail:
            fail.write(f'{host_ip} Не удалось подключиться к CSP')
    except TimeoutError:
        with open('fail.txt', 'a') as fail:
            fail.write(
                f' {host_ip} Попытка установить соединение была безуспешной, т.к. от другого компьютера за требуемое '
                'время не получен нужный отклик')
    except paramiko.ssh_exception.AuthenticationException:
        with open('fail.txt', 'a') as fail:
            fail.write(f'{host_ip} Ошибка авторизации')
    except IndexError:
        cert_create_status[host_ip] = 'Ошибка индексации'
        with open('fail.txt', 'a') as fail:
            fail.write(f'{host_ip} Ошибка индексации, повторите запрос\n')


def get_cert_info(data, index):
    data.send(f'cert_mgr show -i {index}\n')
    time.sleep(2)
    info = data.recv(100000).decode('utf-8')
    # matchd = re.search('(Valid to:) +(?P<date>\w{3} \w{3}\s+\d+ \d+:\d+:\d+ \d+)', cert)
    match = re.search('CN=(?P<cn>\S+)', info)
    matchd = re.search('(Valid to:) +(?P<date>\w{3} \w{3}\s+\d+ \d+:\d+:\d+ \d+)', info)
    date = time.strptime(matchd.group('date'))
    print(f"{match.group('cn')} {time.strftime('%B %d %Y', date)} \n")


def create_request(data, obj, ip):
    data.send(f"cert_mgr create -subj \"{obj}\" -GOST_R3410EL\n")
    time.sleep(2)
    press = data.recv(100000).decode('utf-8')
    if 'Crypto error. Unable to create certificate request' in press:
        print(CRYPT_ERROR)
        cert_create_status[ip] = CRYPT_ERROR
        with open('fail.txt', 'a') as f:
            f.write(f'{ip} {CRYPT_ERROR} \n')
            return CRYPT_ERROR
    while "Press key" in press:
        print(press)
        sleep = random.randint(1, 4)
        prompt = press.split("key:")[-1].strip()
        print(prompt)
        data.send(prompt)
        time.sleep(sleep)
        press = data.recv(100000).decode('utf-8')
    answer = press.split('-----')[2]
    return answer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ip host')
    parser.add_argument('-host', action="store", dest='host')
    parser.add_argument('--info', action="store_true", dest='info')
    parser.add_argument('--file', action="store_true", dest='file')
    host = parser.parse_args().host
    if parser.parse_args().info:
        action = 'info'
    else:
        action = 'get'
    if parser.parse_args().file:
        with open('ip.txt') as iplist:
            for ip in iplist:
                print(ip, end='')
                exec_command_get_cert('10.251.253.243', 'root', base64.b64decode('TG1wbGhtVHVoWTVLM3dLZlZFWEVPc2Zi'),
                                      host_ip=ip.strip(), action=action)
            for key, value in cert_create_status.items():
                print(f'{key} {value}')
    else:
        if host is None:
            host = input('введите ип\n')
            # host = '10.17.4.36'
        exec_command_get_cert('10.251.253.243', 'root', base64.b64decode('TG1wbGhtVHVoWTVLM3dLZlZFWEVPc2Zi'),
                              host_ip=host, action=action)
