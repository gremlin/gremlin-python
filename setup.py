import io
import os
from distutils.file_util import copy_file
from setuptools import setup, find_packages

from gremlinapi.util import get_version


__version__ = get_version()


def getRequires():
    deps = ['requests>=2.22.0', 'urllib3>=1.25.8']
    return deps


dir_path = os.path.abspath(os.path.dirname(__file__))
readme = io.open(os.path.join(dir_path, 'README.md'), encoding='utf-8').read()

setup(
    name='gremlinapi',
    version=str(__version__),
    author='Kyle Hultman',
    author_email='kyle@gremlin.com',
    url='https://github.com/gremlin/gremlin-python/',
    packages=find_packages(exclude=["temp*.py", "test"]),
    include_package_data=True,
    license='Apache 2.0',
    description='Gremlin library for Python',
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=getRequires(),
    python_requires='>=3.6',
    entry_points={"console_scripts": ["pgremlin = gremlinapi.cli:main"]},
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)