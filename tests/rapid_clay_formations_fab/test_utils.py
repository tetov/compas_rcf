from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pytest

from rapid_clay_formations_fab.utils import wrap_list


@pytest.fixture
def list_():
    return list(range(10))


def test_wrap_list(list_):
    assert wrap_list(list_, 25) == list_[25 % len(list_)]
