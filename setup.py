# -*- coding: utf-8 -*-
import os, io
from setuptools import find_packages, setup

BASE_DIR = os.path.join(os.path.dirname(__file__))

with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding="utf-8") as readme:
    README = readme.read()

with io.open(os.path.join(BASE_DIR, 'requirements.txt'), encoding='utf-8') as fh:
    REQUIREMENTS = fh.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='Boorunaut',
    version='0.5.0',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A taggable imageboard built in Django.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/Boorunaut/Boorunaut',
    author='LucasCTN, ThiagoCamposTN',
    author_email='lucascampostn@gmail.com, thiagocampostn@gmail.com',
    entry_points={'console_scripts': [
        'boorunaut=booru.setup.start_project:main',
    ]},
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=REQUIREMENTS,
)