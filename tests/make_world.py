"""Build the ready-to-play world: python3 tests/make_world.py  ->  "Station 9/" and "Station 9.zip"."""
import os
import shutil
import subprocess
import sys
import time
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import server  # noqa: E402

server.stop() if os.path.exists(os.path.join(server.SERVER, "server.pid")) else None
server.setup()
server.start()
from rcon import Rcon  # noqa: E402
r = Rcon()
print(r.cmd("function station9:start"))
time.sleep(15)                               # the rebuild runs over a few dozen ticks
print(r.cmd("function station9:reset"))
print(r.cmd("scoreboard players set #stage s9 0"))
print(r.cmd("save-all flush"))
time.sleep(3)
bad = server.errors()
server.stop()
if bad:
    print("\n".join(bad))
    sys.exit("server reported errors; not packaging")
out = os.path.join(ROOT, "Station 9")
if os.path.exists(out):
    shutil.rmtree(out)
subprocess.check_call([sys.executable, os.path.join(ROOT, "package_world.py"), os.path.join(server.SERVER, "world"), out])
zpath = os.path.join(ROOT, "Station 9.zip")
if os.path.exists(zpath):
    os.remove(zpath)
with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
    for base, _, names in os.walk(out):
        for n in sorted(names):
            full = os.path.join(base, n)
            z.write(full, os.path.relpath(full, ROOT))
print(f"{zpath}: {os.path.getsize(zpath) // 1024} KB")
