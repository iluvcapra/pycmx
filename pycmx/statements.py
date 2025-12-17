# pycmx
# (c) 2025 Jamie Hardt

from typing import Any, NamedTuple

from .cdl import AscSopComponents

# type str = str


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
    line: str
    cdl_sop: AscSopComponents[float]
    line_number: int


class StmtCdlSat(NamedTuple):
    value: float
    line_number: int


class StmtFrmc(NamedTuple):
    start: int
    end: int
    duration: int
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
    delay: str
    line_number: int


class StmtUnrecognized(NamedTuple):
    content: str
    line_number: int


class StmtCorruptRemark(NamedTuple):
    selector: str
    exception: Any
    line_number: int


# StmtMotionMemory = namedtuple(
#     "MotionMemory", ["source", "fps"])  # FIXME needs more fields
