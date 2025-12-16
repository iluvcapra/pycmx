# pycmx
# (c) 2025 Jamie Hardt

from collections import namedtuple

from typing import NamedTuple


class StmtTitle(NamedTuple):
    title: str
    line_number: int


class StmtFCM(NamedTuple):
    drop: bool
    line_number: int


class StmtEvent(NamedTuple):
    event: int
    source: str
    channels: str
    trans: str
    trans_op: str
    source_in: str
    source_out: str
    record_in: str
    record_out: str
    source_field_size: int
    line_number: int


class StmtAudioExt(NamedTuple):
    audio3: bool
    audio4: bool
    line_number: int


class StmtClipName(NamedTuple):
    name: str
    affect: str
    line_number: int


class StmtSourceFile(NamedTuple):
    filename: str
    line_number: int


class StmtCdlSop(NamedTuple):
    slope_r: str
    slope_g: str
    slope_b: str
    offset_r: str
    offset_g: str
    offset_b: str
    power_r: str
    power_g: str
    power_b: str
    line_number: int


class StmtCdlSat(NamedTuple):
    value: str
    line_number: int


class StmtFrmc(NamedTuple):
    start: str
    end: str
    duration: str
    line_number: int


class StmtRemark(NamedTuple):
    text: str
    line_number: int


class StmtEffectsName(NamedTuple):
    name: str
    line_number: int


class StmtSourceUMID(NamedTuple):
    name: str
    umid: str
    line_number: int


class StmtSplitEdit(NamedTuple):
    video: bool
    magnitude: str
    line_number: int


class StmtUnrecognized(NamedTuple):
    content: str
    line_number: int


StmtMotionMemory = namedtuple(
    "MotionMemory", ["source", "fps"])  # FIXME needs more fields
