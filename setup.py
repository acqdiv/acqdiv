from setuptools import setup, find_packages


setup(
    name='acqdiv',
    version='1.0',
    description='Pipeline for ACQDIV project',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
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
        'Bug Reports': 'https://github.com/uzling/acqdiv/issues',
        'Source': 'https://github.com/uzling/acqdiv',
    }
)
