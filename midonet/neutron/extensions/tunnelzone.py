# vim: tabstop=4 shiftwidth=4 softtabstop=4
# Copyright (C) 2014 Midokura SARL.
# All Rights Reserved.
#
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

from neutron.api import extensions
from neutron.api.v2 import base
from neutron import manager
from neutron.openstack.common import log as logging

LOG = logging.getLogger(__name__)

TUNNELZONE = 'tunnelzone'
TUNNELZONES = '%ss' % TUNNELZONE
TUNNELZONE_HOST = 'tunnelzonehost'
TUNNELZONE_HOSTS = '%ss' % TUNNELZONE_HOST

TUNNELZONEHOST_ATTRIBUTE_MAP = {
    'id': {'allow_post': False, 'allow_put': False,
           'validate': {'type:uuid': None}, 'is_visible': True},
    'tunnel_zone_id': {'allow_post': False, 'allow_put': False,
                       'validate': {'type:uuid': None},
                       'is_visible': True},
    'tunnel_zone': {'allow_post': False, 'allow_put': False,
                    'validate': {'type:url': None}, 'is_visible': True},
    'host_id': {'allow_post': True, 'allow_put': True,
                'validate': {'type:uuid': None}, 'is_visible': True},
    'host': {'allow_post': False, 'allow_put': False,
             'validate': {'type:uuid': None}, 'is_visible': True},
    'ip_address': {'allow_post': True, 'allow_put': True,
                   'validate': {'type:ip_address': None}, 'is_visible': True},
    'tenant_id': {'allow_post': True, 'allow_put': False,
                  'required_by_policy': True,
                  'validate': {'type:string': None},
                  'is_visible': True}
}

RESOURCE_ATTRIBUTE_MAP = {
    TUNNELZONES: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:string': None}, 'is_visible': True},
        'name': {'allow_post': True, 'allow_put': True,
                 'validate': {'type:string': None}, 'is_visible': True},
        'type': {'allow_post': True, 'allow_put': True, 'default': 'GRE',
                 'validate': {'type:string': 'GRE'}, 'is_visible': True},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'required_by_policy': True,
                      'validate': {'type:string': None},
                      'is_visible': True}
    }
}


class Tunnelzone(extensions.ExtensionDescriptor):
    """Extension class supporing tunnel zone."""

    @classmethod
    def get_name(cls):
        return "Tunnelzone"

    @classmethod
    def get_alias(cls):
        return 'tunnelzone'

    @classmethod
    def get_description(cls):
        return ("Tunnel zone represents a group in which hosts can be "
                "included to form an isolated zone for tunneling.")

    @classmethod
    def get_namespace(cls):
        return "http://docs.openstack.org/ext/tunnelzone/api/v1.0"

    @classmethod
    def get_updated(cls):
        return "2014-08-28T10:00:00-00:00"

    @classmethod
    def get_resources(cls):
        exts = list()
        plugin = manager.NeutronManager.get_plugin()
        resource_name = TUNNELZONE
        collection_name = TUNNELZONES
        params = RESOURCE_ATTRIBUTE_MAP.get(collection_name, dict())
        controller = base.create_resource(collection_name, resource_name,
                                          plugin, params, allow_bulk=False)
        ex = extensions.ResourceExtension(collection_name, controller)
        exts.append(ex)

        # Tunnel Zone Host
        parent = dict(member_name=resource_name,
                      collection_name=collection_name)
        tunnelzone_plugin = manager.NeutronManager.get_service_plugins().get(
            TUNNELZONE)
        tunnelzonehost_controller = base.create_resource(
            TUNNELZONE_HOSTS, TUNNELZONE_HOST,
            tunnelzone_plugin, TUNNELZONEHOST_ATTRIBUTE_MAP,
            parent=parent, allow_bulk=True)
        tunnelzonehost_extension = extensions.ResourceExtension(
            TUNNELZONE_HOSTS, tunnelzonehost_controller, parent=parent)
        exts.append(tunnelzonehost_extension)

        return exts
