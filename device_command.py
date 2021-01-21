import paramiko
import time


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
        answer = data.recv(100000).decode('utf-8')
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


if __name__ == '__main__':
    exec_command('10.251.253.243', 'root', 'LmplhmTuhY5K3wKfVEXEOsfb')
