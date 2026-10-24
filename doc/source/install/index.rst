====================================
Qinling Dashboard installation guide
====================================

This page describes the manual installation of qinling-dashboard,
while distribution packages may provide more automated process.

.. note::

   This page assumes horizon has been installed.
   Horizon setup is beyond the scope of this page.

Install Qinling Dashboard with all relevant packages to your Horizon environment.

.. code-block:: console

    pip install qinling-dashboard

In most cases, qinling-dashboard is installed into your python "site-packages"
directory like ``/usr/local/lib/python2.7/site-packages``.
We refer to the directory of qinling-dashboard as ``<qinling-dashboard-dir>`` below
and it would be ``<site-packages>/qinling_dashboard`` if installed via pip.
The path varies depending on Linux distribution you use.

To enable qinling-dashboard plugin, you need to put horizon plugin setup files
into horizon "enabled" directory.

The plugin setup files are found in ``<qinling-dashboard-dir>/enabled``.

.. code-block:: console

   $ cp <qinling-dashboard-dir>/enabled/_[1-9]*.py \
         /usr/share/openstack-dashboard/openstack_dashboard/local/enabled

.. note::

   The directory ``local/enabled`` may be different depending on your
   environment or distribution used. The path above is one used in Ubuntu
   horizon package.

Register qinling's policies with OpenStack Dashboard, so that the panels
only offer the actions qinling allows the user, in ``local_settings.py`` or
a file of ``local_settings.d``:

.. code-block:: python

   from qinling_dashboard import conf as qinling_conf
   qinling_conf.register_policies(POLICY_FILES, DEFAULT_POLICY_FILES)

Without it Horizon checks no policy of qinling and every action is offered.
``qinling_dashboard/conf/default_policies/qinling.yaml`` holds qinling's
default policies, ``qinling_dashboard/conf/qinling_policy.yaml`` the
overrides, which should be those of the ``policy.yaml`` qinling uses.

Compile the translation message catalogs of qinling-dashboard.

.. code-block:: console

   $ cd <qinling-dashboard-dir>
   $ python ./manage.py compilemessages

Run the Django update commands.
Note that ``compress`` is required when you enable compression.

.. code-block:: console

   $ cd <horizon-dir>
   $ DJANGO_SETTINGS_MODULE=openstack_dashboard.settings python manage.py collectstatic --noinput
   $ DJANGO_SETTINGS_MODULE=openstack_dashboard.settings python manage.py compress --force

Finally, restart your web server. For example, in case of apache:

.. code-block:: console

   $ sudo service apache2 restart
