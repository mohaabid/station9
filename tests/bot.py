"""Python side of the bot driver: start tests/bot/driver.js, then call methods."""
import json
import os
import socket
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))


class Bot:
    def __init__(self, name="Tester"):
        self.proc = subprocess.Popen(["node", "driver.js", name], cwd=os.path.join(HERE, "bot"),
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for _ in range(200):
            line = self.proc.stdout.readline()
            if "DRIVER READY" in line:
                break
        else:
            raise RuntimeError("bot did not start")
        self.sock = socket.create_connection(("127.0.0.1", 25590), timeout=120)
        self.f = self.sock.makefile("r")

    def __getattr__(self, op):
        def call(**kw):
            self.sock.sendall((json.dumps(dict(op=op, **kw)) + "\n").encode())
            return json.loads(self.f.readline())
        return call

    def close(self):
        try:
            self.proc.terminate()
        except Exception:
            pass
