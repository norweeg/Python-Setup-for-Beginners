import logging
import sys
from os import environ
from pathlib import Path

from menuinst import install

stdout = logging.StreamHandler(sys.stdout)
stdout.addFilter(lambda r: r.levelno < logging.WARNING)
stderr = logging.StreamHandler(sys.stderr)
stderr.setLevel(logging.WARNING)

logging.basicConfig(
    format="%(levelname)s: %(message)s",
    level=logging.INFO,
    handlers=[stdout,stderr],
)


prefix = environ["CONDA_PREFIX"]

for shortcut_file in (Path(prefix)/"Menu").glob("*.json"):
    try:
        install(shortcut_file, prefix)
    except Exception as e:
        logging.warning(f"{shortcut_file} was not able to be installed: {e}")
