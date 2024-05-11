import subprocess

import requests
from bs4 import BeautifulSoup


def install_required_libraries():
    subprocess.run(["pip", "install", "beautifulsoup4"])


def get_latest_version(package_name):
    url = f"https://pypi.org/project/{package_name}/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        latest_version_tag = soup.find('h1', {'class': 'package-header__name'})
        if latest_version_tag:
            latest_version_text = latest_version_tag.text.lower().strip()
            return latest_version_text.split(" ")[1]
    return None


def update_requirements(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if '==' in line:
            package_name, current_version = line.strip().split('==')
            latest_version = get_latest_version(package_name)
            if latest_version and latest_version != current_version:
                print(package_name + ": " + current_version + " > " + latest_version)
                lines[i] = f"{package_name}=={latest_version}\n"
            else:
                print(package_name + ": No updates")

    with open(file_path, 'w') as file:
        file.writelines(lines)


if __name__ == "__main__":
    install_required_libraries()
    update_requirements('requirements.txt')
