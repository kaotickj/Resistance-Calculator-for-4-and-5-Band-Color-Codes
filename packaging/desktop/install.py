"""Per-user source installer. No Qt/PyQt binaries are redistributed."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import venv

VERSION = "3.0.0"
DEFAULT = Path.home() / ".local/share/resistor-calculator" / VERSION
MARKER = "resistor-calculator-install.json"

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, default=DEFAULT)
    parser.add_argument("--no-shortcut", action="store_true")
    parser.add_argument("--uninstall", action="store_true")
    args = parser.parse_args()
    target = args.target.expanduser().absolute()
    desktop = Path.home() / ".local/share/applications/resistor-calculator.desktop"
    if args.uninstall:
        marker = target / MARKER
        if not marker.is_file() or json.loads(marker.read_text())["product"] != "resistor-calculator":
            parser.error("Not a recognized installation; nothing was removed")
        # Delete a shortcut only when it points to this installation.
        if desktop.exists() and str(target) in desktop.read_text():
            desktop.unlink()
        shutil.rmtree(target)
        print("Removed", target)
        return
    if sys.version_info[:2] != (3, 12):
        parser.error("Python 3.12 is required. Install it from python.org or your Linux package manager.")
    if target.exists():
        parser.error(f"{target} already exists. Uninstall that version first or choose another --target.")
    source = Path(__file__).resolve().parent
    target.mkdir(parents=True)
    try:
        for name in ("resistanceCalculator.py", "icon.png", "LICENSE", "THIRD_PARTY_NOTICES.md", "requirements.txt", "install.py", "uninstall.sh", "README.txt"):
            shutil.copy2(source / name, target / name)
        if (source / "icon.ico").exists():
            shutil.copy2(source / "icon.ico", target / "icon.ico")
        venv.EnvBuilder(with_pip=True).create(target / ".venv")
        python = target / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        with (target.parent / "resistor-calculator-install.log").open("w") as log:
            subprocess.run([str(python), "-m", "pip", "install", "--isolated", "--disable-pip-version-check", "--only-binary=:all:", "--index-url", "https://pypi.org/simple", "-r", str(target / "requirements.txt")], stdout=log, stderr=subprocess.STDOUT, check=True)
            subprocess.run([str(python), "-m", "pip", "check"], stdout=log, stderr=subprocess.STDOUT, check=True)
        (target / MARKER).write_text(json.dumps({"product": "resistor-calculator", "version": VERSION}), encoding="utf-8")
        if os.name != "nt":
            # Quote desktop Exec per the freedesktop specification.
            def quote(value):
                return '"' + str(value).replace('\\', '\\\\').replace('"', '\\"').replace('`', '\\`').replace('$', '\\$').replace('%', '%%') + '"'
            launcher = target / "launch.sh"
            launcher.write_text('#!/bin/sh\nHERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)\nexec "$HERE/.venv/bin/python" "$HERE/resistanceCalculator.py" "$@"\n')
            launcher.chmod(0o755)
            (target / "uninstall.sh").chmod(0o755)
            if not args.no_shortcut:
                desktop.parent.mkdir(parents=True, exist_ok=True)
                desktop.write_text('[Desktop Entry]\nType=Application\nName=Resistor Color Code Calculator\nExec=' + quote(launcher) + '\nIcon=' + str(target / 'icon.png') + '\nTerminal=false\nCategories=Education;Science;\n', encoding='utf-8')
        print("Installed", target)
    except BaseException:
        shutil.rmtree(target)
        raise

if __name__ == "__main__":
    main()
