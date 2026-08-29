#!/usr/bin/env python3

'''
One-off generator for the per-service test_<service>.py files in
test/task/int/. Not part of the test suite itself - rerun manually after
adding or removing a service under serv/.
'''

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
SERV_DIR = os.path.join(REPO_ROOT, 'serv')
OUT_DIR = os.path.join(REPO_ROOT, 'test', 'task', 'int')

TEMPLATE = '''#!/usr/bin/env python3

import os
import sys
import unittest

from test.util import engine

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

if __name__ == '__main__':
    unittest.main()

class {class_name}(engine.ComposeIntegrationTestCase):
    service = '{service}'
'''


def class_name_for(service):
    parts = re.split(r'[^a-zA-Z0-9]+', service)
    name = ''.join(part[:1].upper() + part[1:] for part in parts if part)
    return f'Test{name}'


def main():
    services = sorted(
        name for name in os.listdir(SERV_DIR)
        if not name.startswith('@')
        and os.path.isfile(os.path.join(SERV_DIR, name, 'docker-compose.yml'))
    )

    for service in services:
        content = TEMPLATE.format(class_name=class_name_for(service), service=service)
        out_path = os.path.join(OUT_DIR, f'test_{service.replace("-", "_")}.py')
        with open(out_path, 'w') as handle:
            handle.write(content)
        print(f'wrote {out_path}')


if __name__ == '__main__':
    main()
