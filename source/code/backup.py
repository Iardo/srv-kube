import subprocess
from datetime import datetime

from source.core.load import *

from source.head.values import *

class backup:
    '''
    '''
    @staticmethod
    def services():
        for file in os.listdir(values.installed_dir):
            serv_name = file
            manifest, _ = load.yml(values.conf_manifest)
            database = manifest['services'][serv_name]['database'] if manifest['services'][serv_name] else None

            match database:
                case 'postgresql':
                    print(f'{serv_name} - backup')
                    backup.db_postgresql(serv_name)
                case default:    
                    print(f'{serv_name} - database config not found in manifest')

    '''
    '''
    @staticmethod
    def db_postgresql(name: str):
        serv_name = name
        serv_file = f'database.sql'
        serv_archive = f'{datetime.now().strftime("%Y%m%d-%H%M%S")}.tar.gz'
        execute_dump = f'pg_dump -U postgres -h localhost {serv_name} >> /backups/{serv_file}; tar --create --overwrite --gzip -C /backups -f /backups/{serv_archive} {serv_file}; rm -f /backups/{serv_file}'
        
        subprocess.call(['docker', 'exec', '-it', f'{name}-database', 'sh', '-c', execute_dump])
