#!/usr/bin/python

import subprocess

from ansible.module_utils.basic import *  # NOQA

DOCUMENTATION = '''
---
module: add_ppa
author: Stephen Kent
short_description: Add Ubuntu PPA
description: Add Ubuntu PPA using apt-add-repository
options:
  name:
    description:
    - PPA name (e.g. ppa:ansible/ansible)
    type: string
    required: true
'''

EXAMPLES = '''
# Add the ansible PPA
- add_ppa: name=ppa:ansible/ansible
'''

RETURN = '''
stdout:
    description: Standard output from apt-add-repository
    type: string
'''


def main():
    module = AnsibleModule(
        argument_spec={
            'name': {'required': True},
        },
        supports_check_mode=True,
    )

    changed = False
    stdout = ''

    name = module.params['name']
    if name.startswith('ppa:'):
        name = name.split(':', 1)[1]

    # Determine Ubuntu codename to use
    ubuntu_codename = ''
    for fn in ['/etc/lsb-release', '/etc/upstream-release/lsb-release']:
        if not os.path.isfile(fn):
            continue
        with open(fn, 'r') as f:
            lsb_data = {}
            for line in f.read().splitlines():
                key, value = line.strip().split('=', 1)
                lsb_data[key] = value
            if lsb_data.get('DISTRIB_ID') != 'Ubuntu':
                continue
            ubuntu_codename = lsb_data.get('DISTRIB_CODENAME')
            break
    if not ubuntu_codename:
        raise Exception('Unable to determine Ubuntu release codename')

    # Determine ppa target file name for /etc/apt/sources.list.d/
    sources_file_name = '{}-{}.list'.format(name.replace('/', '-'),
                                            ubuntu_codename)

    if not os.path.isfile(os.path.join('/etc/apt/sources.list.d',
                                       sources_file_name)):
        changed = True

    if changed and not module.check_mode:
        stdout = subprocess.check_output(['apt-add-repository', '-y',
                                          'ppa:{}'.format(name)],
                                         stderr=subprocess.STDOUT)

    module.exit_json(
        changed=changed,
        stdout=stdout,
    )

if __name__ == '__main__':
    main()
