import asyncio


def run_server(host="127.0.0.1", port=8888):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        Server,
        host, port
    )
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


class Server(asyncio.Protocol):
    metric_map = dict()

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())

    @staticmethod
    def process_data(data):
        data_arr = data.split()
        try:
            if data_arr[0] == "put":
                key = data_arr[1]
                if key not in Server.metric_map:
                    Server.metric_map[key] = []
                Server.metric_map[key].append((data_arr[2], data_arr[3]))
                ans = "ok\n\n"
            elif data_arr[0] == "get":
                ans = "ok\n"
                if data_arr[1] == "*":
                    for key in Server.metric_map:
                        arr = Server.metric_map[key]
                        for tup in arr:
                            ans += f"{key} {tup[0]} {tup[1]}\n"
                elif data_arr[1] in Server.metric_map:
                    key = data_arr[1]
                    arr = Server.metric_map[key]
                    for tup in arr:
                        ans += f"{key} {tup[0]} {tup[1]}\n"
                ans += "\n"
            else:
                ans = "error\nwrong command\n\n"
        except Exception:
            ans = "error\nwrong command\n\n"
        finally:
            return ans
