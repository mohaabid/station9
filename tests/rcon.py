"""Tiny RCON client for driving the test server."""
import socket
import struct


class Rcon:
    def __init__(self, host="127.0.0.1", port=25575, password="station9"):
        self.sock = socket.create_connection((host, port), timeout=30)
        self._id = 0
        if self._send(3, password)[0] == -1:
            raise RuntimeError("RCON auth failed")

    def _send(self, kind, body):
        self._id += 1
        data = struct.pack("<ii", self._id, kind) + body.encode("utf-8") + b"\x00\x00"
        self.sock.sendall(struct.pack("<i", len(data)) + data)
        size = struct.unpack("<i", self._recv(4))[0]
        rid, _ = struct.unpack("<ii", self._recv(8))
        payload = self._recv(size - 8)[:-2].decode("utf-8", "replace")
        return rid, payload

    def _recv(self, n):
        buf = b""
        while len(buf) < n:
            chunk = self.sock.recv(n - len(buf))
            if not chunk:
                raise ConnectionError("RCON closed")
            buf += chunk
        return buf

    def cmd(self, command):
        return self._send(2, command)[1]

    def close(self):
        self.sock.close()
