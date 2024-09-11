import re
from socketserver import BaseRequestHandler
import os

FLAG = os.environ.get("FLAG", r"flag{echo_test}")


class EchoHandler(BaseRequestHandler):
    def handle(self):
        print(f"Connected from {self.client_address}")
        # try receive first
        data = b""
        try:
            self.request.settimeout(3)
            data: bytes = self.request.recv(1024)
        except TimeoutError:
            pass
        if data and re.match(
            rb"(?P<method>\w+) (?P<url>\S+) (?P<version>HTTP/\d\.\d)", data
        ):
            self.request.sendall(b"HTTP/1.1 418 I'm a teapot\r\n")
            self.request.sendall(b"Content-Type: text/plain\r\n")
            self.request.sendall(b"Content-Encoding: identity\r\n")
            self.request.sendall(b"Connection: close\r\n")
            self.request.sendall(b"\r\n")
            self.request.sendall(b"You have encountered a teapot!\n")
            self.request.sendall(
                b"Please use tools like netcat to connect to this service.\n"
            )
            self.request.sendall(b"Bye!\n")
            self.request.close()
            return
        self.request.sendall(b"Welcome to echo service!\n")
        self.request.sendall(f"{FLAG=}\n".encode())
        while True:
            self.request.sendall(b"> ")
            data = self.request.recv(1024)
            if not data:
                break
            self.request.sendall(data)
        self.request.sendall(b"Bye!\n")
        self.request.close()
