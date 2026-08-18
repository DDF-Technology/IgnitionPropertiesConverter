"""Raccoglie licenze e metadati delle distribuzioni usate dalla release."""

from __future__ import annotations

import argparse
import importlib.metadata as metadata
import shutil
import sys
from pathlib import Path


DISTRIBUTIONS = (
    "pandas",
    "numpy",
    "openpyxl",
    "ttkbootstrap",
    "Pillow",
    "et_xmlfile",
    "python-dateutil",
    "six",
    "tzdata",
    "PyInstaller",
)


def safe_name(value: str) -> str:
    return "".join(character if character.isalnum() or character in "._-" else "_" for character in value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    destination = args.destination.resolve()
    destination.mkdir(parents=True, exist_ok=True)

    inventory: list[str] = []
    for distribution_name in DISTRIBUTIONS:
        distribution = metadata.distribution(distribution_name)
        package_name = distribution.metadata.get("Name", distribution_name)
        package_root = destination / f"{safe_name(package_name)}-{distribution.version}"
        package_root.mkdir(parents=True, exist_ok=True)
        license_expression = distribution.metadata.get("License-Expression") or distribution.metadata.get("License") or "Non dichiarata"
        homepage = distribution.metadata.get("Home-page") or distribution.metadata.get("Project-URL") or "Non dichiarata"
        metadata_text = (
            f"Name: {package_name}\nVersion: {distribution.version}\n"
            f"License: {license_expression}\nOrigin: {homepage}\n"
        )
        (package_root / "PACKAGE-METADATA.txt").write_text(metadata_text, encoding="utf-8")

        copied = 0
        for file in distribution.files or ():
            filename = Path(str(file)).name.lower()
            if not (filename.startswith("license") or filename.startswith("copying") or filename.startswith("notice")):
                continue
            source = Path(distribution.locate_file(file))
            if not source.is_file():
                continue
            target = package_root / f"{copied:02d}-{safe_name(Path(str(file)).name)}"
            shutil.copy2(source, target)
            copied += 1
        inventory.append(f"{package_name} {distribution.version} — {license_expression}")

    python_license = Path(sys.base_prefix) / "LICENSE.txt"
    if python_license.is_file():
        shutil.copy2(python_license, destination / "PYTHON-LICENSE.txt")
    for relative, target_name in (("tcl/tcl8.6/license.terms", "TCL-LICENSE.txt"), ("tcl/tk8.6/license.terms", "TK-LICENSE.txt")):
        source = Path(sys.base_prefix) / relative
        if source.is_file():
            shutil.copy2(source, destination / target_name)

    (destination / "INVENTORY.txt").write_text("\n".join(inventory) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
