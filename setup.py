import io
import os
from distutils.file_util import copy_file
from setuptools import setup, find_packages


__version__ = None
with open('sendgrid/version.py') as f:
    exec(f.read())

def getRequires():
    deps = ['python_http_client>=3.2.1']
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
    install_requires=getRequires(),
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)