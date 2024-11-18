import json
import socket
import threading
from CProtocol import *

# виртуальные функции

protocol = CProtocol()

# events
NEW_CONNECTION: int = 1
CLOSE_CONNECTION: int = 2
NEW_REGISTRATION: int = 3

class CServerBL:

    def __init__(self, host, port):

        # Open the log file in write mode, which truncates the file to zero length
        with open(LOG_FILE, 'w'):
            pass  # This block is empty intentionally

        self._host = host
        self._port = port
        self._server_socket = None
        self._is_srv_running = True
        self._client_handlers = []
        self._register_clients = []




    def delete_from_client_handlers(self, address):
        write_to_log(f"[CServer_BL] client_handlers list length: {len(self._client_handlers)}")
        for el in self._client_handlers:
            if el._address == address:
                write_to_log(f"[CServer_BL] in delete client, el found: {el._address}")
                self._client_handlers.remove(el)
                self._is_srv_running = False
        write_to_log(f"[CServer_BL] el deleted, list: {len(self._client_handlers)}")
    def stop_server(self):
        try:
            self._is_srv_running = False
            # Close server socket
            if self._server_socket is not None:
                self._server_socket.close()
                self._server_socket = None
            write_to_log(f"[CSERVERBL] in stop_server: {len(self._client_handlers)}")
            if len(self._client_handlers) > 0:
                # Waiting to close all opened threads
                for client_thread in self._client_handlers:
                    client_thread.join()
                write_to_log(f"[SERVER_BL] All Client threads are closed")
            write_to_log(f"[CServerBL] srv_socket in stop server: {self._server_socket}")

        except Exception as e:
            write_to_log("[SERVER_BL] Exception in Stop_Server fn : {}".format(e))

    def start_server(self):
        try:
            self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._server_socket.bind((self._host, self._port))
            self._server_socket.listen(5)
            write_to_log(f"[SERVER_BL] listening...")
            self._is_srv_running = True

            if self._is_srv_running and self._server_socket is not None:
                write_to_log(f"[CServerBL] server_socket : {self._server_socket}")
                # Accept socket request for connection
                client_socket, address = self._server_socket.accept()
                write_to_log(f"[SERVER_BL] Client connected {client_socket}{address} ")
                write_to_log(f"[SERVER_BL address: {address}")
                # Start Thread
                cl_handler = CClientHandler(client_socket, address, self.fire_event, self.delete_from_client_handlers, self._register_clients, self.fire_event, self.register)
                cl_handler.start()
                self._client_handlers.append(cl_handler)
                write_to_log(f"[SERVER_BL] ACTIVE CONNECTION {threading.active_count() - 1}")
                # invoke event NEW CONNECTION
                self.fire_event(NEW_CONNECTION, cl_handler)
                write_to_log("[SERVER_BL] NEW CONNECTION event invoked")


        # ??? something happens here
        # except Exception as e:
        #     write_to_log("[SERVER_BL] Exception in start_server fn : {}".format(e))
        finally:
            write_to_log(f"[SERVER_BL] Server thread is DONE")

    def fire_event(self, enum_event: int, client_handl):
        pass

    def register(self, login, password):
        pass

class CClientHandler(threading.Thread):

    _client_socket = None
    _address = None

    def __init__(self, client_socket, address, fn, del_fn, reg_cl, fire_ev, reg):
        super().__init__()
        self.fire_event = fn
        self._client_socket = client_socket
        self._address = address
        self.del_fn = del_fn
        self.reg_cl = reg_cl
        self.fire_event = fire_ev
        self.register = reg

    def run(self):
        # This code run in separate thread for every client
        connected = True
        while connected:
            # 1. Get message from socket and check it
            valid_msg, msg = receive_msg(self._client_socket)
            if valid_msg:
                # 2. Save to log
                write_to_log(f"[SERVER_BL] received from {self._address}] - {msg}")
                if len(msg) > 4:
                    cmd, args = CProtocol27().parse_request(msg)
                    write_to_log("[CServerBL] args: " + args + "; cmd: " + cmd)
                else:
                    cmd = msg
                # 3. If valid command - create response
                if check_cmd(cmd):
                    if check_cmd(cmd) == 1:
                        pr26 = CProtocol26()
                        # 4. Create response
                        response = pr26.create_response_msg(msg)
                        # 5. Save to log
                        write_to_log("[SERVER_BL] send from PR26- " + response)
                    elif check_cmd(cmd) == 2:
                        pr27 = CProtocol27()
                        # 4. Create response
                        response = pr27.create_response_msg(cmd, args)
                        # 5. Save to log
                        write_to_log("[SERVER_BL] send from PR27- " + response)
                        if cmd == "REG":
                            args_json = json.loads(args)
                            # check if client is already in the list 2
                            is_InList2 = False
                            for el in self.reg_cl:
                                if el == self._client_socket:
                                    write_to_log("f[CServerBL] client is already in the list")
                                    is_InList2 = True
                            if not is_InList2:
                                self.reg_cl.append(self._client_socket)
                                write_to_log(f"[CServerBL] REG LIST: {self.reg_cl}")
                                self.fire_event(NEW_REGISTRATION, self)
                                arr = []
                                index = 0
                                for item in args_json.values():
                                    arr.insert(index, item)
                                    index += 1
                                write_to_log(f"[CServerBL] login: {arr[0]}, password: {arr[1]}")
                                login_bytes = str.encode(arr[0])
                                password_bytes = str.encode(arr[1])
                                write_to_log(
                                    f"[CServerBL] login_bytes: {login_bytes}; password_bytes: {password_bytes}")
                                self.register(login_bytes, password_bytes)





                    # 6. Send response to the client
                    self._client_socket.send(response.encode(FORMAT))
                else:
                    # if received command not supported by protocol, just send it back "as is"
                    # 4. Create response
                    response = "Non-supported cmd"
                    response = f"{len(response):02d}{response}"
                    # 5. Save to log
                    write_to_log("[SERVER_BL] send - " + response)
                    # 6. Send response to the client
                    self._client_socket.send(response.encode(FORMAT))

                # Handle DISCONNECT command
                if msg == DISCONNECT_MSG:

                    connected = False

        # invoke CLOSE CONNECTION event
        self.fire_event(CLOSE_CONNECTION, self)
        self._client_socket.close()
        self.del_fn(self._address)
        write_to_log(f"[SERVER_BL] Thread closed for : {self._address} ")


if __name__ == "__main__":
    write_to_log(f"{SERVER_HOST} {PORT}")
    server = CServerBL(SERVER_HOST, PORT)
    server.start_server()
