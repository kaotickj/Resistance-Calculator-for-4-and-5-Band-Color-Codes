#!/bin/sh
set -eu
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec python3.12 "$HERE/install.py" --uninstall --target "$HERE"
