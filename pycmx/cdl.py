# pycmx
# (c) 2025 Jamie Hardt

from dataclasses import dataclass
from typing import Generic, NamedTuple, TypeVar

T = TypeVar('T')


@dataclass
class Rgb(Generic[T]):
    """
    A tuple of three `T`s, where each is the respective red, green and blue
    values of interest. 
    """

    red: T #: Red component
    green: T #: Green component
    blue: T #: Blue component


@dataclass
class AscSopComponents(Generic[T]):
    """
    Fields in an ASC SOP (Slope-Offset-Power) color transfer function
    statement.

    The ASC SOP is a transfer function of the form:

    :math:`y_{color} = (ax_{color} + b)^p`

    for each color component the source, where the `slope` is `a`, `offset`
    is `b` and `power` is `p`.
    """

    slope: Rgb[T] #: The linear/slope component `a`
    offset: Rgb[T] #: The constant/offset component `b`
    power: Rgb[T] #: The exponential/power component `p`


class FramecountTriple(NamedTuple):
    """
    Fields in an FRMC statement
    """

    start: int
    end: int
    duration: int
