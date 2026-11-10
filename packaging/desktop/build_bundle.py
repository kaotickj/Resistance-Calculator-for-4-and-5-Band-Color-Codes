"""Build source-only installer payload. Run from repository root."""
from pathlib import Path
import shutil
import tarfile

root = Path.cwd()
stage = root / 'stage'
if stage.exists():
    shutil.rmtree(stage)
stage.mkdir()
for name in ('resistanceCalculator.py', 'icon.png', 'LICENSE'):
    shutil.copy2(root / name, stage / name)
if (root / 'icon.ico').exists():
    shutil.copy2(root / 'icon.ico', stage / 'icon.ico')
for name in ('install.py', 'install.sh', 'uninstall.sh', 'requirements.txt', 'THIRD_PARTY_NOTICES.md', 'README.txt'):
    shutil.copy2(root / 'packaging/desktop' / name, stage / name)
(root / 'dist').mkdir(exist_ok=True)
with tarfile.open(root / 'dist/ResistorCalculator-3.0.0-linux-x86_64-installer.tar.gz', 'w:gz') as archive:
    archive.add(stage, arcname='ResistorCalculator-3.0.0')
