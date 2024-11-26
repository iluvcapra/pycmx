# -*- coding: utf-8 -*-
"""
pycmx is a parser for CMX 3600-style EDLs.

This module (c) 2023 Jamie Hardt. For more information on your rights to
copy and reuse this software, refer to the LICENSE file included with the
distribution.
"""

__version__ = '1.2.2'

from .parse_cmx_events import parse_cmx3600
from .transition import Transition
from .event import Event
from .edit import Edit
