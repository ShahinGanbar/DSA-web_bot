import requests

def is_valid_pypi_package(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    resp = requests.get(url)
    return resp.status_code == 200

# Example:
module = "sklearn"
pip_package = module if is_valid_pypi_package(module) else "scikit-learn"
print()
