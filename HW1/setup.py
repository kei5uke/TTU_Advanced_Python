from gettext import install
import setuptools

from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name = "triangle_kekonn",
    version="0.0.3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    auther="Keisuke Konno",
    author_email="kekonn@ttu.ee",
    packages=["triangle_kekonn"]
)