# change release number in setup.py

Tag commit and push:

```
git tag -a v1.1.0 -m "release 1.1.0"
git push --tags
```

Create fresh copy of the repository to avoid adding unnecessary or even
sensitive data!

Upload to PyPI:

```shell
mkdir acqdiv-release
cd acqdiv-release
git clone git@github.com:acqdiv/acqdiv.git
python3 -m venv venv
. venv/bin/activate
cd acqdiv
python setup.py sdist
pip install twine
twine upload dist/*
```
