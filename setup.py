from setuptools import setup, find_packages


requires = [
    # list required third-party packages here
    'sqlalchemy',
]

setup(
    name='acqdiv',
    version='0.0',
    description='python package for the acqdiv project',
    long_description='',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    author='',
    author_email='',
    url='',
    keywords='data linguistics',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=[],
    test_suite="acqdiv"
)
