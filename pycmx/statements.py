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
    format: int
    line_number: int


StmtAudioExt = namedtuple("AudioExt", ["audio3", "audio4", "line_number"])
StmtClipName = namedtuple("ClipName", ["name", "affect", "line_number"])
StmtSourceFile = namedtuple("SourceFile", ["filename", "line_number"])
StmtCdlSop = namedtuple("CdlSop", ['slope_r', 'slope_g', 'slope_b',
                                   'offset_r', 'offset_g', 'offset_b',
                                   'power_r', 'power_g', 'power_b',
                                   'line_number'])
StmtCdlSat = namedtuple("CdlSat", ['value', 'line_number'])
StmtFrmc = namedtuple("Frmc", ['start', 'end', 'duration', 'line_number'])
StmtRemark = namedtuple("Remark", ["text", "line_number"])
StmtEffectsName = namedtuple("EffectsName", ["name", "line_number"])
StmtSourceUMID = namedtuple("Source", ["name", "umid", "line_number"])
StmtSplitEdit = namedtuple("SplitEdit", ["video", "magnitude", "line_number"])
StmtMotionMemory = namedtuple(
    "MotionMemory", ["source", "fps"])  # FIXME needs more fields
StmtUnrecognized = namedtuple("Unrecognized", ["content", "line_number"])
