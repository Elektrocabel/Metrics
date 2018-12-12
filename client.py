import socket
import time


class ClientError(Exception):
    '''A Client Error occurred.'''


class Client:
    def __init__(self, host="127.0.0.1", port=8888, timeout=None):
        self.sock = socket.create_connection((host, port), timeout)

    def __del__(self):
        self.sock.close()

    def put(self, key, value, timestamp=int(time.time())):
        req = f"put {key} {str(value)} {str(timestamp)}\n"
        self.sock.sendall(req.encode())
        if "\n\n" not in self.sock.recv(1024).decode():
            raise ClientError

    def get(self, key):
        req = f"get {key}\n"
        self.sock.sendall(req.encode())
        data = self.sock.recv(1024).decode()
        try:
            data_list = data.split(sep="\n")[1:-2]
            metric_map = dict()
            for line in data_list:
                s = line.split()
                if s[0] not in metric_map:
                    metric_map[s[0]] = []
                metric_map[s[0]].append((int(s[2]), float(s[1])))
            return metric_map
        except Exception:
            raise ClientError
