"""Run the official 1.20.4 server for automated tests.

    python3 tests/server.py setup      # fresh void world with the datapack installed
    python3 tests/server.py start      # start in the background, wait until it's up
    python3 tests/server.py stop
    python3 tests/server.py errors     # print datapack load errors from the log

The server lives in $S9_SERVER_DIR (default ~/.station9-server) and needs server.jar
(1.20.4, sha1 8dd1a28015f51b1803213892b50b7b4fc76e594d) there. Running it means
accepting the Minecraft EULA, which setup does by writing eula.txt.
"""
import os
import re
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SERVER = os.path.expanduser(os.environ.get("S9_SERVER_DIR", "~/.station9-server"))
LOG = os.path.join(SERVER, "logs", "latest.log")
PROPS = {
    "level-type": "minecraft\\:flat",
    "generator-settings": '{"layers":[{"block":"minecraft:air","height":1}],"biome":"minecraft:the_void","features":false}',
    "enable-rcon": "true", "rcon.password": "station9", "rcon.port": "25575",
    "online-mode": "false", "gamemode": "adventure", "difficulty": "normal",
    "spawn-protection": "0", "spawn-monsters": "false", "spawn-animals": "false", "spawn-npcs": "false",
    "view-distance": "8", "simulation-distance": "8", "server-port": "25565",
    "max-tick-time": "-1", "sync-chunk-writes": "false",
}


def setup():
    world = os.path.join(SERVER, "world")
    if os.path.exists(world):
        shutil.rmtree(world)
    os.makedirs(os.path.join(world, "datapacks"))
    shutil.copytree(os.path.join(ROOT, "Station9"), os.path.join(world, "datapacks", "Station9"))
    res = os.path.join(ROOT, "build", "resources.zip")
    if os.path.exists(res):
        shutil.copy(res, os.path.join(world, "resources.zip"))
    with open(os.path.join(SERVER, "eula.txt"), "w") as f:
        f.write("eula=true\n")
    with open(os.path.join(SERVER, "server.properties"), "w") as f:
        f.writelines(f"{k}={v}\n" for k, v in PROPS.items())
    for name in ("ops.json", "whitelist.json"):
        p = os.path.join(SERVER, name)
        if os.path.exists(p):
            os.remove(p)


def start(timeout=180):
    out = open(os.path.join(SERVER, "console.txt"), "w")
    proc = subprocess.Popen(["java", "-Xmx3G", "-jar", "server.jar", "nogui"], cwd=SERVER,
                            stdin=subprocess.PIPE, stdout=out, stderr=subprocess.STDOUT)
    with open(os.path.join(SERVER, "server.pid"), "w") as f:
        f.write(str(proc.pid))
    t0 = time.time()
    while time.time() - t0 < timeout:
        if proc.poll() is not None:
            sys.exit("server exited early; see console.txt")
        if os.path.exists(LOG) and "RCON running" in open(LOG, errors="replace").read():
            return
        time.sleep(1)
    sys.exit("server did not come up")


def stop():
    try:
        from rcon import Rcon
        Rcon().cmd("stop")
    except Exception:
        pid = open(os.path.join(SERVER, "server.pid")).read().strip()
        subprocess.call(["kill", pid])
    time.sleep(6)


def errors():
    text = open(LOG, errors="replace").read()
    bad = [l for l in text.splitlines()
           if re.search(r"Failed to load function|Couldn't load|Failed to parse|Unknown or incomplete|Exception", l)]
    return bad


if __name__ == "__main__":
    sys.path.insert(0, HERE)
    what = sys.argv[1]
    if what == "setup":
        setup()
    elif what == "start":
        start()
    elif what == "stop":
        stop()
    elif what == "errors":
        bad = errors()
        print("\n".join(bad) if bad else "no load errors")
        sys.exit(1 if bad else 0)
