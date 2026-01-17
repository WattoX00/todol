import sys
import requests
import subprocess
from importlib.metadata import version, PackageNotFoundError

PACKAGE_NAME = "todol"

def main():
    try:
        installed_version = version(PACKAGE_NAME)
    except PackageNotFoundError:
        installed_version = "not installed"

    try:
        resp = requests.get(f"https://pypi.org/pypi/{PACKAGE_NAME}/json", timeout=3)
        resp.raise_for_status()
        latest_version = resp.json()["info"]["version"]
    except Exception:
        latest_version = "unknown"

    if installed_version == latest_version:
        print(f"{PACKAGE_NAME} {installed_version} Your packages are up to date")
    else:
        print(f"{PACKAGE_NAME} {installed_version} (newer version available: {latest_version})")

        update_question = input("Do you want to update it now? [Y/n]: ").strip().lower()
        if update_question in ("", "y", "yes"):
            try:
                print("Running: pipx upgrade todol")
                subprocess.run(["pipx", "upgrade", PACKAGE_NAME], check=True)
                print("Update completed!")
            except FileNotFoundError:
                print("pipx not found. Please install it first: https://pipx.pypa.io/latest/installation/")
            except subprocess.CalledProcessError:
                print("Update failed. Try running the command manually: pipx upgrade todol")

    sys.exit(0)
