import os
import shutil
import glob

try:
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fail_hosts.txt')
    os.remove(path)
except FileNotFoundError:
    pass
try:
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fail_import.txt')
    os.remove(path)
except FileNotFoundError:
    pass
try:
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'import_status.txt')
    os.remove(path)
except FileNotFoundError:
    pass
try:
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'success_hosts.txt')
    os.remove(path)
except FileNotFoundError:
    pass

for f in glob.glob("/srv/nfs/shares/hosts_certs3.1/*"):
    try:
            shutil.rmtree(f)
    except NotADirectoryError:
        os.remove(f)








    