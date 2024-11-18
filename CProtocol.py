import logging
import socket
from abc import ABC

# prepare Log file
LOG_FILE = 'LOG.log'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Open the log file in write mode, which truncates the file to zero length
with open(LOG_FILE, 'w'):  # write in log file and delete all that was there before
    pass

SERVER_HOST: str = "0.0.0.0"
CLIENT_HOST: str = "127.0.0.1"
PORT: int = 12345
BUFFER_SIZE: int = 1024
HEADER_LEN: int = 4  # !!!
FORMAT: str = 'utf-8'

# Protocol26 and 27
Cpr26 = ["TIME", "NAME", "RAND", "EXIT"]
Cpr27 = ["DIR", "DELETE", "SEND_PHOTO", "EXECUTE", "TAKE_SCREENSHOT", "COPY", "REG"]

DISCONNECT_MSG: str = "EXIT"


def write_to_log(msg):
    logging.info(msg)
    print(msg)


def check_cmd(data) -> int:
    data = data.upper()
    if data == DISCONNECT_MSG:
        return 1
    elif data in Cpr26:
        return 1
    elif data in Cpr27:
        return 2
    else:
        return 0


def receive_msg(my_socket: socket):
    # receive msg from client or server
    """Extract message from protocol, without the length field
       If length field does not include a number, returns False, "Error" """
    str_header = my_socket.recv(HEADER_LEN).decode()
    write_to_log(f"[Protocol - GET_MSG] str_header - {str_header}")
    if str_header == '': return False, ''
    length = int(str_header)
    write_to_log(f"[Protocol - GET_MSG] length - {length}")
    if length > 0:
        buf = my_socket.recv(length).decode()
    else:
        return False, ''

    return True, buf


class CProtocol(ABC):

    def __init__(self):
        super().__init__()

    def create_request_msg(self, cmd) -> str:
        pass

    def create_response_msg(self, cmd, args='') -> str:
        pass
