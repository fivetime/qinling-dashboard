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

import os
import re
import types
from unittest import mock

from django import test
from django.test.utils import override_settings
from openstack_auth import policy
import yaml

import qinling_dashboard
from qinling_dashboard import conf as qinling_conf

# keystone expands implied roles into the token.
ROLES = {
    'reader': ['reader'],
    'member': ['member', 'reader'],
    'admin': ['admin', 'manager', 'member', 'reader'],
}


class RegisterPoliciesTest(test.SimpleTestCase):

    def test_register(self):
        policy_files = {'identity': 'keystone_policy.yaml'}
        default_policy_files = {}

        qinling_conf.register_policies(policy_files, default_policy_files)

        self.assertEqual(qinling_conf.POLICY_FILE,
                         policy_files['function_engine'])
        self.assertEqual(qinling_conf.DEFAULT_POLICY_FILE,
                         default_policy_files['function_engine'])
        self.assertEqual('keystone_policy.yaml', policy_files['identity'])

    def test_default_policies(self):
        with open(qinling_conf.DEFAULT_POLICY_FILE) as f:
            rules = {p['name']: p for p in yaml.safe_load(f)}

        self.assertEqual(48, len(rules))
        self.assertIn('role:member', rules['function:create']['check_str'])
        self.assertIn('role:reader', rules['function:get_all']['check_str'])
        self.assertEqual(['project'], rules['function:create']['scope_types'])

    def test_panels_use_known_rules(self):
        with open(qinling_conf.DEFAULT_POLICY_FILE) as f:
            known = {p['name'] for p in yaml.safe_load(f)}
        top = os.path.dirname(qinling_dashboard.__file__)
        used = set()
        for path, _, files in os.walk(os.path.join(top, 'content')):
            for name in files:
                if name.endswith('.py'):
                    with open(os.path.join(path, name)) as f:
                        used |= set(re.findall(
                            r'"function_engine", "([^"]+)"', f.read()))

        self.assertNotEqual(set(), used)
        self.assertEqual(set(), used - known)


class HorizonPolicyCheckTest(test.SimpleTestCase):
    """The checks the panels make, by Horizon's own policy engine."""

    def setUp(self):
        super(HorizonPolicyCheckTest, self).setUp()
        policy_files, default_policy_files = {}, {}
        qinling_conf.register_policies(policy_files, default_policy_files)
        override = override_settings(POLICY_FILES=policy_files,
                                     DEFAULT_POLICY_FILES=default_policy_files,
                                     POLICY_DIRS={},
                                     POLICY_FILES_PATH='/')
        override.enable()
        self.addCleanup(override.disable)
        policy.reset()
        self.addCleanup(policy.reset)

    def _allowed(self, persona, rule):
        # Not a Mock: Horizon caches the credentials in an attribute.
        user = types.SimpleNamespace(
            id='USER', username='user', project_id='PROJECT',
            project_name='project', is_superuser=False,
            user_domain_id='default', domain_id=None,
            roles=[{'name': r} for r in ROLES[persona]])
        request = mock.Mock(user=user, session={})
        # Horizon takes the user from the session.
        with mock.patch('openstack_auth.utils.get_user', return_value=user):
            return policy.check((('function_engine', rule),), request)

    def test_reader(self):
        for rule in ('function:get_all', 'function:get', 'execution:get_all',
                     'execution:log_show', 'runtime:get_all'):
            self.assertTrue(self._allowed('reader', rule), rule)
        for rule in ('function:create', 'function:update', 'function:delete',
                     'function_version:create', 'execution:create',
                     'execution:delete', 'runtime:create'):
            self.assertFalse(self._allowed('reader', rule), rule)

    def test_member(self):
        for rule in ('function:create', 'function:update', 'function:delete',
                     'function_version:create', 'function_version:delete',
                     'execution:create', 'execution:delete'):
            self.assertTrue(self._allowed('member', rule), rule)
        for rule in ('runtime:create', 'function:scale_up',
                     'function:get_all:all_projects'):
            self.assertFalse(self._allowed('member', rule), rule)

    def test_admin(self):
        self.assertTrue(self._allowed('admin', 'runtime:create'))
        self.assertTrue(self._allowed('admin', 'function:create'))
