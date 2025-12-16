# pycmx
# (c) 2025 Jamie Hardt

from typing import Generic, NamedTuple, TypeVar

T = TypeVar('T')


class Rgb(NamedTuple, Generic[T]):
    red: T
    green: T
    blue: T


class AscSopComponents(NamedTuple, Generic[T]):
    """
    Fields in an ASC SOP (Slope-Offset-Power) color transfer function 
    statement
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
