from setuptools import setup, find_packages

try:
    with open('README.md') as file:
        long_description = file.read()
except UnicodeDecodeError:
    long_description = ''
except FileNotFoundError:
    long_description = ''

requirements = [
    'fastapi == 0.60.1',
    'loguru == 0.5.3',
    'gunicorn == 20.0.4',
    'uvicorn == 0.10.3',
    'requests==2.25.1',
    'python-dotenv==0.15.0',
]

setup(
    name='Mercado BTC Price Monitor',
    version='0.0.1',
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements
)
