#   Copyright 2021 Red Hat, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

from oslo_config import cfg
import oslo_messaging

from directord import drivers


class Driver(drivers.BaseDriver):
    def __init__(
        self, interface, args, encrypted_traffic_data, connection_string
    ):
        super(Driver, self).__init__(
            args=args,
            encrypted_traffic_data=encrypted_traffic_data,
            connection_string=connection_string,
            interface=interface,
        )
        self.mode = getattr(args, "mode", None)
        self.connection_string = connection_string
        self.conf = cfg.CONF
        self.conf.transport_url = "amqp://{}:5672//".format(
            self.interface.bind_address
        )
        self.transport = oslo_messaging.get_rpc_transport(self.conf)
