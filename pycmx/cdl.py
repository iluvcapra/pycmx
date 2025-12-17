# pycmx
# (c) 2025 Jamie Hardt

from dataclasses import dataclass
from typing import Generic, NamedTuple, TypeVar

T = TypeVar('T')


@dataclass
class Rgb(Generic[T]):
    red: T
    green: T
    blue: T


@dataclass
class AscSopComponents(Generic[T]):
    """
    Fields in an ASC SOP (Slope-Offset-Power) color transfer function
    statement.

    The ASC SOP is a transfer function of the form:

    :math:`y_color = (ax_color + b)^p`

    for each color component the source, where the `slope` is `a`, `offset`
    is `b` and `power` is `p`.
    """
    slope: Rgb[T]
    offset: Rgb[T]
    power: Rgb[T]


class FramecountTriple(NamedTuple):
    """
    Fields in an FRMC statement
    """
    start: int
    end: int
    duration: int
