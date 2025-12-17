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
