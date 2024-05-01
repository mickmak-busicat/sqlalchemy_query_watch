from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

VERSION = "0.0.1"
DESCRIPTION = "Subscribe query log to SqlAlchemy event"

setup(
    name="sqlalchemy_query_watch",
    version=VERSION,
    author="Mick Mak",
    author_email="mk.triniti@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["sqlalchemy>=2.0.18"],
    keywords=["python", "sqlalchemy", "log"],
)
