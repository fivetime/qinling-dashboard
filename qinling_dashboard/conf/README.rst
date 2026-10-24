================
Qinling policies
================

Horizon offers an action only when the policy of qinling allows it to the
user, but it reads the policies of a service only when ``POLICY_FILES``
names it. Register qinling's from a snippet in ``local_settings.d``::

    from qinling_dashboard import conf as qinling_conf
    qinling_conf.register_policies(POLICY_FILES, DEFAULT_POLICY_FILES)

``default_policies/qinling.yaml`` holds qinling's defaults. Regenerate it
with ``tools/generate_default_policies.py`` in an environment where qinling
is installed whenever qinling's policies change.

``qinling_policy.yaml`` holds the overrides; keep it the same as the
``policy.yaml`` qinling uses, or pass the path of that file as
``policy_file`` to ``register_policies()``.
