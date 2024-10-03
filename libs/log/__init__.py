import json
import socket
from datetime import datetime
import threading
from threading import current_thread


class Log:
    __log_type = None

    def __init__(self, log_type):
        self.__log_type = log_type + "--" + socket.gethostname()

    def info(self, message, extra=None, time=None):
        self.print_log(message, "INFO", extra, time)

    def error(self, message, extra=None, time=None):
        self.print_log(message, "ERROR", extra, time)

    def warn(self, message, extra=None, time=None):
        self.print_log(message, "WARNING", extra, time)

    def print_log(self, message, log_level, extra, time):
        obj_log = {
            "date": datetime.now().astimezone().isoformat(),
            "thread": threading.current_thread().getName(),
            "log_type": self.__log_type,
            "log_level": log_level,
        }
        if time:
            obj_log["time"] = str((datetime.now() - time).total_seconds())
        obj_log["msg"] = message if isinstance(message, str) else str(message)
        if extra is not None:
            for key, value in extra.items():
                obj_log[key] = value
        print(json.dumps(obj_log))