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
"""Qinling's policies for Horizon.

Horizon checks the policies of a service only when POLICY_FILES names it;
otherwise every check of that service passes and the panels offer actions
the API then refuses. Register them from a local_settings.d snippet:

    from qinling_dashboard import conf as qinling_conf
    qinling_conf.register_policies(POLICY_FILES, DEFAULT_POLICY_FILES)
"""
import os

# The scope the panels pass to the policy checks, as in
# ``policy.ifAllowed({rules: [["function_engine", "function:create"]]})``.
POLICY_SCOPE = 'function_engine'

_CONF_DIR = os.path.dirname(os.path.abspath(__file__))
# qinling's defaults, generated from its policy-in-code.
DEFAULT_POLICY_FILE = os.path.join(_CONF_DIR, 'default_policies',
                                   'qinling.yaml')
# Overrides on top of them; keep it in step with the policy.yaml of qinling.
POLICY_FILE = os.path.join(_CONF_DIR, 'qinling_policy.yaml')


def register_policies(policy_files, default_policy_files,
                      policy_file=POLICY_FILE):
    """Add qinling to Horizon's POLICY_FILES and DEFAULT_POLICY_FILES.

    :param policy_file: Path of the overrides, when they live elsewhere
                        (the policy.yaml qinling uses, say).
    """
    policy_files[POLICY_SCOPE] = policy_file
    default_policy_files[POLICY_SCOPE] = DEFAULT_POLICY_FILE
