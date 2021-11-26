from setuptools import setup, find_packages
from api import __version__


try:
    with open('README.md') as file:
        long_description = file.read()
except UnicodeDecodeError:
    long_description = ''
except FileNotFoundError:
    long_description = ''

requirements = [
    'fastapi==0.61.1',
    'loguru==0.5.3',
    'gunicorn==20.0.4',
    'uvicorn==0.15.0',
    'requests==2.25.1',
    'python-dotenv==0.19.1',
]

setup(
    name='Mercado BTC Price Monitor',
    version=__version__,
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements
)
