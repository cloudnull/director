import argparse
import glob
import json
import os

import director

from director import manager


class User(manager.Interface):
    """Director User interface class."""

    def __init__(self, args):
        """Initialize the User interface class.

        Sets up the user object.

        :param args: Arguments parsed by argparse.
        :type args: Object
        """

        super(User, self).__init__(args=args)

    def sanitized_args(self, execute):
        """Return arguments in a flattened array.

        This will inspect the execution arguments and return everything found
        as a flattened array.

        :param execute: Execution string to parse.
        :type execute: String
        :returns: List
        """

        return [i for g in execute for i in g.split()]

    def format_exec(self, verb, execute, target=None, uuid=None):
        """Return a JSON encode object for task execution.

        While formatting the message, the method will treat each verb as a
        case and parse the underlying sub-command, formatting the information
        into a dictionary.

        :param verb: Action to parse.
        :type verb: String
        :param execute: Execution string to parse.
        :type execute: String
        :param target: Target argent to send job to.
        :type target: String
        :param uuid: (optional) Set the job id.
        :type uuid: String
        :returns: String
        """

        parser = argparse.ArgumentParser(description="Process exec commands")
        self.log.debug("Executing - VERB:%s, EXEC:%s", verb, execute)
        if verb == "RUN":
            data = {"command": " ".join(execute)}
        elif verb in ["COPY", "ADD"]:
            parser.add_argument("--chown")
            parser.add_argument("file_path", nargs="+")
            args = parser.parse_args(self.sanitized_args(execute=execute))
            data = dict()
            if args.chown:
                chown = args.chown.split(":", 1)
                if len(chown) == 1:
                    chown.append(None)
                data["user"], data["group"] = chown
            file_from, data["to"] = args.file_path
            data["from"] = [
                i for i in glob.glob(file_from) if os.path.isfile(i)
            ]
            if not data["from"]:
                raise AttributeError(
                    "The value of {} was not found.".format(file_from)
                )
        elif verb == "FROM":
            raise NotImplementedError()
        elif verb == "ARG":
            raise NotImplementedError()
        elif verb == "ENV":
            raise NotImplementedError()
        elif verb == "LABEL":
            raise NotImplementedError()
        elif verb == "USER":
            raise NotImplementedError()
            parser.add_argument("user")
            args = parser.parse_args(self.sanitized_args(execute=execute))
            user = args.user.split(":", 1)
            data = dict()
            if len(user) == 1:
                user.append(None)
            data["user"], data["group"] = user
        elif verb == "EXPOSE":
            raise NotImplementedError()
            parser.add_argument("expose")
            args = parser.parse_args(self.sanitized_args(execute=execute))
            expose = args.expose.split("/", 1)
            data = dict()
            if len(expose) == 1:
                expose.append("tcp")
            data["port"], data["proto"] = expose
        elif verb == "WORKDIR":
            parser.add_argument("workdir")
            args = parser.parse_args(self.sanitized_args(execute=execute))
            data = dict(workdir=args.workdir)
        else:
            raise SystemExit("No known verb defined.")

        if target:
            data["target"] = target

        if uuid:
            data["task"] = uuid

        return json.dumps(data)

    def send_data(self, data):
        """Send data to the socket path.

        The send method takes serialized data and submits it to the given
        socket path.

        This method will return information provided by the server in
        String format.

        :returns: String
        """

        with director.UNIXSocketConnect(self.args.socket_path) as s:
            s.sendall(data.encode())
            return s.recv(1024000).decode()


class Manage(User):
    """Director Manage interface class."""

    def __init__(self, args):
        """Initialize the Manage interface class.

        Sets up the manage object.

        :param args: Arguments parsed by argparse.
        :type args: Object
        """

        super(User, self).__init__(args=args)

    def run(self):
        """Send the management command to the server.

        :returns: String
        """

        if self.args.list_jobs:
            manage = "list-jobs"
        elif self.args.list_nodes:
            manage = "list-nodes"
        elif self.args.purge_jobs:
            manage = "purge-jobs"
        elif self.args.purge_nodes:
            manage = "purge-nodes"
        else:
            raise SystemExit("No known management function was defined.")

        self.log.debug("Executing Management Command:%s", manage)
        return self.send_data(data=json.dumps(dict(manage=manage)))
