# pycmx
# (c) 2018 Jamie Hardt

from collections import namedtuple

from .parse_cmx_statements import (parse_cmx3600_statements, StmtEvent,StmtFCM )
from .edit_list import EditList

def parse_cmx3600(f):
    """
    Parse a CMX 3600 EDL.

    Args:
        f : a file-like object, anything that's readlines-able.

    Returns:
        An :class:`EditList`.
    """
    statements = parse_cmx3600_statements(f)
    return EditList(statements)
    
