from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in frappe_auth/__init__.py
from frappe_auth import __version__ as version

setup(
	name="frappe_auth",
	version=version,
	description="Frappe Authenticator for Mobile Apps",
	author="White Hat Global",
	author_email="rk@whitehatglobal.org",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
