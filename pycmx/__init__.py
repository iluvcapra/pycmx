# -*- coding: utf-8 -*-
"""
pycmx is a module for parsing CMX 3600-style EDLs. For more information and
examples see README.md

This module (c) 2018 Jamie Hardt. For more information on your rights to
copy and reuse this software, refer to the LICENSE file included with the
distribution.
"""

__version__ = '1.1.0'
__author__  = 'Jamie Hardt'

from .parse_cmx_events import parse_cmx3600
from .transition import Transition
from .event import Event
from .edit import Edit
