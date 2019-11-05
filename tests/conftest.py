import pathlib

import pytest


@pytest.fixture(scope="class")
def tests_dir(request):
    request.cls.tests_dir = pathlib.Path(__file__).parent


@pytest.fixture(scope="class")
def dummy_cha(request):
    request.cls.dummy_cha_path = str(
        pathlib.Path(__file__).parent / 'unittests/chat/test_files/dummy.cha')

