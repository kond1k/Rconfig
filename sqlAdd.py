import SQL_commands
from datetime import datetime


def create_command_for_new_device(ip):
    sqlid = SQL_commands.get_max_id() + 1
    ipsplit = ip.split('.')
    command = '''INSERT INTO nodes (id,deviceName, deviceUsername, devicePassword,
 deviceEnablePassword, deviceIpAddr, devicePrompt, deviceEnablePrompt, nodeCatId, templateId, vendorId,
  model, nodeAddedBy, defaultCreds, deviceDateAdded, custom_GROUP )'''
    sql_exec = f''' VALUES (
{sqlid}, 'CC48-0{ipsplit[2]}BDR01', 'rconfig', 'S3U3YzBOR1VLUmJUbjJ0YkJxOWZWaXNnVWlSOFVpc2ZvTXladFdnMVNVaz0=', '', 
'48.0.{ipsplit[2]}.254', '<0{ipsplit[2]}BDR01>', '', 12, 5, '2', 'AR201','kondyukov', 0,
 '{datetime.now().strftime('%Y-%m-%d')}','48/REGION');'''
    command_exec = command + sql_exec
    return command_exec


if __name__ == '__main__':
    sql_command = create_command_for_new_device('48.0.99.254')
    print(SQL_commands.insert_device(sql_command))

'''INSERT INTO `nodes` VALUES
 (23, '2', '2', '2', '2', 'CC48-011BDR01', 'rconfig', 'S3U3YzBOR1VLUmJUbjJ0YkJxOWZWaXNnVWlSOFVpc2ZvTXladFdnMVNVaz0=', '',
'48.0.11.254', '<011BDR01>', '', 12, 5, '2', 'AR201', NULL, 'kondyukov', 0, NULL, NULL, NULL, '2021-01-14', NULL, 1,
'48/REGION'),'''

'''
mysql> INSERT INTO 'nodes' ('id ','deviceName', 'deviceUsername', 'devicePassword',
 'deviceEnablePassword', 'deviceIpAddr', 'devicePrompt', 'deviceEnablePrompt', 'nodeCatId', 'templateId', 'vendorId',
  'model', 'nodeAddedBy', 'defaultCreds', 'deviceDateAdded', 'custom_GROUP' ) VALUES(col2*2,15);

[(1, ' id '),
 (2, ' taskId412827 '),
 (3, ' taskId515833 '),
 (4, ' taskId197117 '),
 (5, ' taskId344198 '),
 (6, ' deviceName    '),
 (7, ' deviceUsername '),
 (8, ' devicePassword '),
 (9, ' deviceEnablePassword '),
 (10, ' deviceIpAddr '),
 (11, ' devicePrompt '),
 (12, ' deviceEnablePrompt '),
 (13, ' nodeCatId '), - Category
 (14, ' templateId '), - template
 (15, ' vendorId '), 1 - Cisco, 2 - Huawei 
 (16, ' model  '),
 (17, ' nodeVersion '),
 (18, ' nodeAddedBy '),
 (19, ' defaultCreds '),
 (20, ' defaultUsername '),
 (21, ' defaultPassword '),
 (22, ' defaultEnablePassword '),
 (23, ' deviceDateAdded '),
 (24, ' deviceLastUpdated '),
 (25, ' status '),
 (26, ' custom_GROUP ')]
'''
