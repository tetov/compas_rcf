from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys

if sys.version_info.major < 3:
    from .py2_funcs import *  # noqa: F401,F403
else:
    from .py3_funcs import *  # noqa: F401,F403
