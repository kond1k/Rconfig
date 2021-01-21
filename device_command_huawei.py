import paramiko
import time
from device_command import exec_command

command_for_create_user = "system-view\naaa\nlocal-user rconfig3 password irreversible-cipher 5bWqIGe7rPIBMrq1kJkc " \
                          "privilege level " \
                          "2\nlocal-user rconfig3 service-type telnet terminal ssh\ncommand-privilege level 2 view " \
                          "cli_8f display " \
                          "current-configuration\ndisplay version\n save\nY\n"

command_for_get_info = "dis ver\n \n"


def get_info_from_device(ip, user, password):
    info = exec_command(ip, user, password, command_to_device=command_for_get_info)
    if info:
        info_str = info.split('\n')
        model = []
        for line in info_str:
            if 'Board' in line:
                model.append(line.split(':')[-1].strip())
        prompt = info_str[-1]
        device_name = prompt[1:-1]
        return ip, device_name, prompt, model[0]
    else:
        print(f'с ип {ip} произошла ошибка, подробности в файле')


if __name__ == '__main__':
    # answer = exec_command('48.0.78.254', , , command_to_device=command_for_get_info)
    print(get_info_from_device('48.0.78.254', 'admin', '1qazxsw2'))
