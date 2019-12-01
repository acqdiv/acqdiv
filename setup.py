from setuptools import setup, find_packages


setup(
    name='acqdiv',
    version='1.0.0',
    description='Pipeline for the ACQDIV database',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/acqdiv/acqdiv',
    author='ACQDIV developer team',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    keywords='data linguistics',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'sqlalchemy',
        'lxml',
        'tqdm',
        'python-dateutil'
    ],
    extras_require={
        'dev': ['pandas', 'numpy', 'tox'],
        'test':  ['pytest'],
    },
    entry_points={
        'console_scripts': ['acqdiv=acqdiv.__main__:main'],
    },
    project_urls={
        'Bug Reports': 'https://github.com/acqdiv/acqdiv/issues',
        'Source': 'https://github.com/acqdiv/acqdiv',
    }
)
