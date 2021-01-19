import paramiko
import time

command_for_create_user = "system-view\naaa\nlocal-user rconfig3 password irreversible-cipher 5bWqIGe7rPIBMrq1kJkc " \
                          "privilege level " \
                          "2\nlocal-user rconfig3 service-type telnet terminal ssh\ncommand-privilege level 2 view " \
                          "cli_8f display " \
                          "current-configuration\ndisplay version\n save\nY\n"

command_for_get_info = "dis ver\n"


def exec_command(host, user, secret, port=22, command_to_device=''):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host, password=secret,
                       username=user, port=port, allow_agent=False, look_for_keys=False)
        data = client.invoke_shell()
        time.sleep(1)
        data.send(command_to_device)
        time.sleep(5)
        answer = data.recv(10000).decode('utf-8')
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


def get_info_from_device():
    info = exec_command('48.0.78.254', 'admin', '1qazxsw2', command_to_device=command_for_get_info)
    prompt = answer.split('\n')[-1]
    return prompt


if __name__ == '__main__':
    answer = exec_command('48.0.78.254', 'admin', '1qazxsw2', command_to_device=command_for_get_info)
    prompt =
    print(prompt)
