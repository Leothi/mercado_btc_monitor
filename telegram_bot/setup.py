from setuptools import setup, find_packages

__version__ = '0.0.1'

try:
    with open('README.md') as file:
        long_description = file.read()
except UnicodeDecodeError:
    long_description = ''
except FileNotFoundError:
    long_description = ''

requirements = [
    'loguru == 0.5.3',
    'python-dotenv==0.15.0',
    'python-telegram-bot==13.1',
    'requests==2.25.1',
    'pydantic == 1.7.3'
]

setup(
    name='Telegram BTC BOT',
    version=__version__,
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements
)
