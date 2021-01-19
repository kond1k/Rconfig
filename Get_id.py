import pymysql
from sshtunnel import SSHTunnelForwarder

ssh_host = '100.64.0.17'
ssh_port = 22
ssh_user = 'root'
ssh_password = 'Sph@era92'
sql_hostname = 'localhost'
sql_username = 'root'
sql_password = '4xMJt1WIHvCGvwViDWPIXJ27'
sql_main_database = 'rconfig'
sql_port = 3306


def get_max_id():
    with SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_password=ssh_password,
            remote_bind_address=(sql_hostname, sql_port)) as tunnel:
        conn = pymysql.connect(host=sql_hostname, user=sql_username,
                               passwd=sql_password, db=sql_main_database, port=tunnel.local_bind_port)
        query = 'SELECT id from nodes order by id desc limit 1;'
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        return data[0][0]


if __name__ == '__main__':
    id = get_max_id()
    print(id)
