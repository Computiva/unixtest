# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages

setup(
    name = "unixtest",
    version = "0.1.0",
    author = "Ângelo Nuffer",
    author_email = "angelonuffer@gmail.com",
    packages = find_packages(),
    entry_points = """
        [console_scripts]
        unixtest = unixtest:main
    """,
)
