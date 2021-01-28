import paramiko
import time
import base64
import argparse
import random



def exec_command(host, user, secret, port=22, command_to_device=''):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host, password=secret,
                       username=user, port=port, allow_agent=False, look_for_keys=False)
        data = client.invoke_shell()
        time.sleep(2)
        data.send(command_to_device)
        time.sleep(2)
        answer = data.recv(1000000).decode('utf-8')
        return answer
        # with open(f'hosts/success/{host}.txt', 'w') as suc:
        #     suc.write(answer)
        # client.close()
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


def exec_command_get_cert(host, user, secret, port=22, command_to_device='', host_ip=''):
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
        data.send("123qweASD\n")
        time.sleep(2)
        data.send("cert_mgr show\n")
        time.sleep(2)
        local = data.recv(100000).decode('utf-8').split("\n")
        for cert in local:
            if 'local' in cert:
                answer = cert
                index = answer.split(' ')[0]
                obj = answer.split('local')[-1].strip()
                break
        time.sleep(2)
        data.send(f"cert_mgr create -subj \"{obj}\" -GOST_R3410EL\n")
        time.sleep(2)
        press = data.recv(100000).decode('utf-8')
        while "Press key" in press:
            print(press)
            sleep = random.randint(1, 6)
            prompt = press.split("key:")[-1].strip()
            print(prompt)
            data.send(prompt)
            time.sleep(sleep)
            press = data.recv(100000).decode('utf-8')
        answer = press.split('-----')[2]
        return answer
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
    parser = argparse.ArgumentParser(description='ip host')
    parser.add_argument('-host', action="store", dest='host')
    host = parser.parse_args().host
    with open(f'{host}.txt', 'w') as f:
        a = exec_command_get_cert('10.251.253.243', 'root', 'LmplhmTuhY5K3wKfVEXEOsfb',
                                  host_ip=host)
        f.write(a)
        print("Complete")
