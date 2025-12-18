# pycmx
# (c) 2018-2025 Jamie Hardt

from typing import TextIO

from .parse_cmx_statements import (parse_cmx3600_statements)
from .edit_list import EditList


def parse_cmx3600(f: TextIO, tolerant: bool = False) -> EditList:
    """
    Parse a CMX 3600 EDL.

    :param TextIO f: a file-like object, an opened CMX 3600 .EDL file.
    :param bool tolerant: If `True`, a relaxed event line recognition method 
        will be used in the case the stricter default method fails.
    :returns: An :class:`pycmx.edit_list.EditList`.
    """
    statements = parse_cmx3600_statements(f, tolerant)
    return EditList(statements)
