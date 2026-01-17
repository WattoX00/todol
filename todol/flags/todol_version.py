import sys
import requests
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
        print(f"{PACKAGE_NAME} {installed_version} LTS")
    else:
        print(f"{PACKAGE_NAME} {installed_version} newer version available: {latest_version}")
    
    sys.exit(0)
