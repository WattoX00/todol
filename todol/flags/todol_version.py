import requests
from importlib.metadata import version, PackageNotFoundError

PACKAGE_NAME = "todol"

class TodolVersion:
    @staticmethod
    def get_installed():
        try:
            return version(PACKAGE_NAME)
        except PackageNotFoundError:
            return "not installed"

    @staticmethod
    def get_latest_online():
        try:
            resp = requests.get(
                f"https://pypi.org/pypi/{PACKAGE_NAME}/json",
                timeout=1
            )
            resp.raise_for_status()
            return resp.json()["info"]["version"]
        except Exception:
            return None

    @staticmethod
    def version():
        installed = TodolVersion.get_installed()
        latest = TodolVersion.get_latest_online()

        if latest is None:
            return f"{PACKAGE_NAME} {installed}"

        if installed == latest:
            return f"{PACKAGE_NAME} {installed} LTS"
        else:
            return f"{PACKAGE_NAME} {installed} (new: {latest})"
