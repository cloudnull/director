#   Copyright Peznauts <kevin@cloudnull.com>. All Rights Reserved.
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

import time


class BaseDriver:
    nullbyte = b"\000"  # Signals null
    heartbeat_ready = b"\001"  # Signals worker is ready
    heartbeat_notice = b"\005"  # Signals worker heartbeat
    job_ack = b"\006"  # Signals job started
    job_end = b"\004"  # Signals job ended
    job_processing = b"\026"  # Signals job running
    job_failed = b"\025"  # Signals job failed
    transfer_start = b"\002"  # Signals start file transfer
    transfer_end = b"\003"  # Signals start file transfer

    def __init__(self, args, encrypted_traffic) -> None:
        """Initialize the Driver.

        :param args: Arguments parsed by argparse.
        :type args: Object
        "param encrypted_traffic: Enable|Disable encrypted traffic.
        :type encrypted_traffic: Boolean
        """

        pass

    def socket_bind(self, socket_type, connection, port, poller_type):
        """Return a socket object which has been bound to a given address.

        When the socket_type is not PUB or PUSH, the bound socket will also be
        registered with self.driver.poller as defined within the Interface
        class.

        :param socket_type: Set the Socket type, typically defined using a
                            constant.
        :type socket_type: Integer
        :param connection: Set the Address information used for the bound
                           socket.
        :type connection: String
        :param port: Define the port which the socket will be bound to.
        :type port: Integer
        :returns: Object
        """

        pass

    def socket_connect(
        self,
        socket_type,
        connection,
        port,
        poller_type,
        send_ready,
    ):
        """Return a socket object which has been bound to a given address.

        When send_ready is set True and the socket_type is not SUB or PULL,
        the bound socket will send a single SOH ready message.

        > A connection back to the server will wait 10 seconds for an ack
          before going into a retry loop. This is done to forcefully cycle
          the connection object to reset.

        :param socket_type: Set the Socket type, typically defined using a
                            constant.
        :type socket_type: Integer
        :param connection: Set the Address information used for the bound
                           socket.
        :type connection: String
        :param port: Define the port which the socket will be bound to.
        :type port: Integer
        :returns: Object
        """

        pass

    def socket_send(
        self,
        socket,
        identity=None,
        msg_id=None,
        control=None,
        command=None,
        data=None,
        info=None,
        stderr=None,
        stdout=None,
    ):
        """Send a message over a socket.

        All message information is assumed to be byte encoded.

        All possible control characters are defined within the Interface class.
        For more on control characters review the following
        URL(https://donsnotes.com/tech/charsets/ascii.html#cntrl).

        :param socket: Socket object.
        :type socket: Object
        :param identity: Target where message will be sent.
        :type identity: Bytes
        :param msg_id: ID information for a given message. If no ID is
                       provided a UUID will be generated.
        :type msg_id: Bytes
        :param control: ASCII control charaters.
        :type control: Bytes
        :param command: Command definition for a given message.
        :type command: Bytes
        :param data: Encoded data that will be transmitted.
        :type data: Bytes
        :param info: Encoded information that will be transmitted.
        :type info: Bytes
        :param stderr: Encoded error information from a command.
        :type stderr: Bytes
        :param stdout: Encoded output information from a command.
        :type stdout: Bytes
        """

        pass

    @staticmethod
    def socket_recv(socket):
        """Receive a message over a socket.

        :param socket: socket object.
        :type socket: Object
        """

        pass

    def job_connect(self):
        """Connect to a job socket and return the socket.

        :returns: Object
        """

        pass

    def transfer_connect(self):
        """Connect to a transfer socket and return the socket.

        :returns: Object
        """

        pass

    def heartbeat_connect(self):
        """Connect to a heartbeat socket and return the socket.

        :returns: Object
        """

        pass

    def heartbeat_bind(self):
        """Bind an address to a heartbeat socket and return the socket.

        :returns: Object
        """

        pass

    def job_bind(self):
        """Bind an address to a job socket and return the socket.

        :returns: Object
        """

        pass

    def transfer_bind(self):
        """Bind an address to a transfer socket and return the socket.

        :returns: Object
        """

        pass

    @property
    def bind_check(self, bind, interval=1):
        """Return True if a bind type contains work ready.

        :param bind: A given Socket bind to identify.
        :type bind: Object
        :param interval: Interval used to determine the polling duration for a
                         given socket.
        :type interval: Integer
        :returns: Object
        """

        pass

    def key_generate(self, keys_dir, key_type):
        pass

    def get_heartbeat(self, interval=0):
        """Return a new hearbeat interval time.

        :param interval: Padding for heartbeat interval.
        :type interval: Integer|Float
        :returns: Float
        """

        return time.time() + interval

    def get_expiry(self, heartbeat_interval=60, interval=1):
        """Return a new expiry time.

        :param interval: Exponential back off for expiration.
        :type interval: Integer|Float
        :returns: Float
        """

        return time.time() + (heartbeat_interval * interval)