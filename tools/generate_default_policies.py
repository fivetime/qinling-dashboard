#!/usr/bin/env python3
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""Write qinling's default policies for Horizon.

Run in an environment where qinling is installed:

    python tools/generate_default_policies.py

The format is that of Horizon's ``manage.py dump_default_policies``.
"""
import os

from oslo_policy import generator
import yaml

OUTPUT = os.path.join(os.path.dirname(__file__), os.pardir,
                      'qinling_dashboard', 'conf', 'default_policies',
                      'qinling.yaml')
HEADER = ('# Default policies of qinling, generated from its policy-in-code '
          'by\n# tools/generate_default_policies.py. Do not edit.\n')


class _NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def main():
    policies = []
    for default in generator.get_policies_dict(['qinling'])['qinling']:
        policies.append({
            'name': default.name,
            'check_str': default.check_str,
            'description': default.description,
            'operations': getattr(default, 'operations', []),
            'scope_types': getattr(default, 'scope_types', None),
        })
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(HEADER)
        yaml.dump(policies, f, Dumper=_NoAliasDumper)
    print('%d policies written to %s' % (len(policies),
                                         os.path.normpath(OUTPUT)))


if __name__ == '__main__':
    main()
