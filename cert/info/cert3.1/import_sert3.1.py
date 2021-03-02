import paramiko
import time
import argparse
import random
import base64
import re
import os
from pathlib import Path

cert_valid_dict = {}
cert_import_status = {}  # конечный статус операции
CRYPT_ERROR = 'Ошибка криптографии'
CONNECT_ERROR = 'Ошибка подключения'
VERSION_ERROR = 'Не подходящий алгоритм шифрования, используйте другой скрипт'


def exec_command_get_cert(host, user, secret, cn, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host, password=secret,
                       username=user, port=port, allow_agent=False, look_for_keys=False)
        data = client.invoke_shell()
        a,b,c,d = host.split('.')
        time.sleep(2)
        data.send('mount -t nfs 10.252.253.245:/srv/nfs/shares/hosts_certs3.1/ -o rw,proto=tcp,soft,nolock /media \n')
        time.sleep(2)
        data.send(f'cp -r /media/{b}g{c}.000 /var/opt/cprocsp/keys\n')
        time.sleep(2)
        data.send(f"cert_mgr import -f /media/{cn}.cer -kc 'hdimage\\{b} {c}.000'\n")
        time.sleep(2)
        data.send('umount /media\n')
        press = data.recv(100000).decode('utf-8')
        answer = re.search(r'cert_mgr import -f /media/\S+ -l.?(?P<status>.+)', press, flags = re.DOTALL)
        cert_import_status[host] = answer['status']
        with open(f'import_status.txt', 'a') as f:
            f.write( f"{host} {answer['status']}\n")

    except paramiko.ssh_exception.NoValidConnectionsError:
        with open('fail_import.txt', 'a') as fail:
            fail.write(f'{host} Не удалось подключиться к CSP')
    except TimeoutError:
        with open('fail_import.txt', 'a') as fail:
            cert_import_status[host] = 'Не удалось подключиться'
            fail.write(
                f' {host} Попытка установить соединение была безуспешной, т.к. от другого компьютера за требуемое '
                'время не получен нужный отклик\n')
    except paramiko.ssh_exception.AuthenticationException:
        with open('fail_import.txt', 'a') as fail:
            fail.write(f'{host} Ошибка авторизации')
    except (IndexError, TypeError):
        cert_import_status[host] = 'Ошибка индексации'
        with open('fail_import.txt', 'a') as fail:
            fail.write(f'{host} Ошибка индексации, повторите запрос\n')



if __name__ == '__main__':
    os.system("openssl pkcs7 -inform DER -outform PEM -in /srv/nfs/shares/hosts_certs3.1/certs.p7b -print_certs > /srv/nfs/shares/hosts_certs3.1/certificate_bundle.cer")
    with open("/srv/nfs/shares/hosts_certs3.1/certificate_bundle.cer") as f:
        a = f.read().split("\n\n")
        for cert in a:
            hostname = re.search(r'subject=.+CN=(\S+)', cert)
            if hostname:
                with open(f'/srv/nfs/shares/hosts_certs3.1/{hostname.group(1)}.cer','w') as fc:
                    fc.write(cert)

    with open('ip3.1.txt') as iplist:
        for host in iplist:
            ipadr, cn = host.split()
            print(ipadr, cn)
            exec_command_get_cert(ipadr.strip(), 'root', base64.b64decode('MTIzcXdlQVNE'), cn)
        for key, value in cert_import_status.items():
            print(f'{key} {value}')

