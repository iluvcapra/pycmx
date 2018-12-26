# -*- coding: utf-8 -*-
"""
pycmx is a module for parsing CMX 3600-style EDLs. For more information and 
examples see README.md

This module (c) 2018 Jamie Hardt. For more information on your rights to 
copy and reuse this software, refer to the LICENSE file included with the 
distribution.
"""



from .parse_cmx_events import parse_cmx3600, Transition, Event, Edit
from . import parse_cmx_events

__version__ = '0.7'
