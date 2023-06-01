# pycmx
# (c) 2018 Jamie Hardt

# from collections import namedtuple

from .parse_cmx_statements import (parse_cmx3600_statements)
from .edit_list import EditList

from typing import TextIO 

def parse_cmx3600(f: TextIO):
    """
    Parse a CMX 3600 EDL.

    :param TextIO f: a file-like object, anything that's readlines-able.
    :returns: An :class:`pycmx.edit_list.EditList`.
    """
    statements = parse_cmx3600_statements(f)
    return EditList(statements)
    
