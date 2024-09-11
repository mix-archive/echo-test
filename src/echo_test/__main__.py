from socketserver import ThreadingTCPServer
import sys

from echo_test import EchoHandler


def main(host: str, port: int) -> int:
    with ThreadingTCPServer(
        (host, port), EchoHandler, bind_and_activate=False
    ) as server:
        server.allow_reuse_address = True
        server.server_bind()
        server.server_activate()
        print(f"Listening on {host}:{port}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
    return 0


if __name__ == "__main__":
    program_name, *args = sys.argv
    if len(args) != 2:
        print(f"Usage: {program_name} <host> <port>")
        sys.exit(1)
    host, port = args
    sys.exit(main(host, int(port)))
