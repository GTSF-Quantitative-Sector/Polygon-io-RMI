from setuptools import setup

VERSION = "1.0"
DESCRIPTION = "Fetch RSI and RMI for a stock using Polygon.io API."

setup(
    name="rmi",
    version=VERSION,
    author="John Washburne",
    author_email="johnwashburne@outlook.com",
    description=DESCRIPTION,
    packages=["rmi"],
    install_requires=[
        "aiohttp",
        "aiosignal",
        "async-timeout",
        "attrs",
        "charset-normalizer",
        "frozenlist",
        "idna",
        "multidict",
        "numpy",
        "yarl",
    ],
)
