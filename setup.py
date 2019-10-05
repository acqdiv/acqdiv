from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='acqdiv',
    version='1.0',
    description='Pipeline for ACQDIV project',
    long_description=long_description,
    url='https://github.com/uzling/acqdiv',
    author='ACQDIV developer team',
    author_email='steven.moran@uzh.ch',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'License :: Free For Educational Use',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='data linguistics',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'sqlalchemy',
        'lxml',
        'tqdm',
        'python-dateutil'
    ],
    extras_require={
        'dev': ['pandas', 'numpy'],
        'test':  ['pytest'],
    },
    entry_points={
        'console_scripts': ['acqdiv=acqdiv.__main__:main'],
    },
    project_urls={
        'Bug Reports': 'https://github.com/uzling/acqdiv/issues',
        'Source': 'https://github.com/uzling/acqdiv',
    }
)
