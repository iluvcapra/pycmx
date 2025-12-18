# pycmx
# (c) 2018-2025 Jamie Hardt

import re
from typing import TextIO, List

from pycmx.cdl import AscSopComponents, Rgb

from .statements import (StmtCdlSat, StmtCdlSop, StmtCorruptRemark, StmtFrmc,
                         StmtRemark, StmtTitle, StmtUnrecognized, StmtFCM,
                         StmtAudioExt, StmtClipName, StmtEffectsName,
                         StmtEvent, StmtSourceFile, StmtSplitEdit)
from .util import collimate


def parse_cmx3600_statements(file: TextIO,
                             tolerant: bool = False) -> List[object]:
    """
    Return a list of every statement in the file argument.
    """
    lines = file.readlines()
    return [_parse_cmx3600_line(line.strip(), line_number, tolerant)
            for (line_number, line) in enumerate(lines)]


def _edl_column_widths(event_field_length, source_field_length) -> List[int]:
    return [event_field_length, 2, source_field_length, 1,
            4, 2,  # chans
            4, 1,  # trans
            3, 1,  # trans op
            11, 1,
            11, 1,
            11, 1,
            11]

# def _edl_m2_column_widths():
#     return [2, # "M2"
#             3,3, #
#             8,8,1,4,2,1,4,13,3,1,1]


def _parse_cmx3600_line(line: str, line_number: int,
                        tolerant: bool = False) -> object:
    """
    Parses a single CMX EDL line.

    :param line: A single EDL line.
    :param line_number: The index of this line in the file.
    """
    event_num_p = re.compile(r"^(\d+)  ")
    line_matcher = event_num_p.match(line)

    if line.startswith("TITLE:"):
        return _parse_title(line, line_number)
    if line.startswith("FCM:"):
        return _parse_fcm(line, line_number)
    if line_matcher is not None:
        event_field_len = len(line_matcher.group(1))

        source_field_len = len(line) - (event_field_len + 65)

        try:
            return _parse_columns_for_standard_form(line, event_field_len,
                                                    source_field_len,
                                                    line_number)

        except EventFormError:
            if tolerant:
                return _parse_columns_tolerant(line, line_number)
            else:
                return StmtUnrecognized(line, line_number)

    if line.startswith("AUD"):
        return _parse_extended_audio_channels(line, line_number)
    if line.startswith("*"):
        return _parse_remark(line[1:].strip(), line_number)
    if line.startswith(">>> SOURCE"):
        return _parse_source_umid_statement(line, line_number)
    if line.startswith("EFFECTS NAME IS"):
        return _parse_effects_name(line, line_number)
    if line.startswith("SPLIT:"):
        return _parse_split(line, line_number)
    if line.startswith("M2"):
        pass
        # return _parse_motion_memory(line, line_number)

    return _parse_unrecognized(line, line_number)


def _parse_title(line, line_num) -> StmtTitle:
    title = line[6:].strip()
    return StmtTitle(title=title, line_number=line_num)


def _parse_fcm(line, line_num) -> StmtFCM:
    val = line[4:].strip()
    if val == "DROP FRAME":
        return StmtFCM(drop=True, line_number=line_num)

    return StmtFCM(drop=False, line_number=line_num)


def _parse_extended_audio_channels(line, line_number):
    content = line.strip()
    audio3 = "3" in content
    audio4 = "4" in content

    if audio3 or audio4:
        return StmtAudioExt(audio3, audio4, line_number)
    else:
        return StmtUnrecognized(line, line_number)


def _parse_remark(line, line_number) -> object:
    if line.startswith("FROM CLIP NAME:"):
        return StmtClipName(name=line[15:].strip(), affect="from",
                            line_number=line_number)
    elif line.startswith("TO CLIP NAME:"):
        return StmtClipName(name=line[13:].strip(), affect="to",
                            line_number=line_number)
    elif line.startswith("SOURCE FILE:"):
        return StmtSourceFile(filename=line[12:].strip(),
                              line_number=line_number)
    elif line.startswith("ASC_SOP"):
        group_patterns: list[str] = re.findall(r'\((.*?)\)', line)

        v1: list[list[tuple[str, str]]] = \
                [re.findall(r'(-?\d+(\.\d+)?)', a) for a in group_patterns]

        v: list[list[str]] = [[a[0] for a in b] for b in v1]

        if len(v) != 3 or any([len(a) != 3 for a in v]):
            return StmtRemark(line, line_number)

        else:
            try:
                return StmtCdlSop(cdl_sop=AscSopComponents(
                    slope=Rgb(red=float(v[0][0]), green=float(v[0][1]),
                              blue=float(v[0][2])),
                    offset=Rgb(red=float(v[1][0]), green=float(v[1][1]),
                               blue=float(v[1][2])),
                    power=Rgb(red=float(v[2][0]), green=float(v[2][1]),
                              blue=float(v[2][2]))
                ),
                    line_number=line_number)

            except ValueError as e:
                return StmtCorruptRemark('ASC_SOP', e, line_number)

    elif line.startswith("ASC_SAT"):
        value = re.findall(r'(-?\d+(\.\d+)?)', line)

        if len(value) != 1:
            return StmtRemark(line, line_number)

        else:
            try:
                return StmtCdlSat(value=float(value[0][0]),
                                  line_number=line_number)

            except ValueError as e:
                return StmtCorruptRemark('ASC_SAT', e, line_number)

    elif line.startswith("FRMC"):
        match = re.match(r'^FRMC START:\s*(\d+)\s+FRMC END:\s*(\d+)'
                         r'\s+FRMC DURATION:\s*(\d+)', line, re.IGNORECASE)

        if match is None:
            return StmtCorruptRemark('FRMC', None, line_number)

        else:
            try:
                return StmtFrmc(start=int(match.group(1)),
                                end=int(match.group(2)),
                                duration=int(match.group(3)),
                                line_number=line_number)
            except ValueError as e:
                return StmtCorruptRemark('FRMC', e, line_number)

    else:
        return StmtRemark(text=line, line_number=line_number)


def _parse_effects_name(line, line_number) -> StmtEffectsName:
    name = line[16:].strip()
    return StmtEffectsName(name=name, line_number=line_number)


def _parse_split(line: str, line_number):
    split_type = line[10:21]
    is_video = split_type.startswith("VIDEO")

    split_delay = line[24:35]
    return StmtSplitEdit(video=is_video, delay=split_delay,
                         line_number=line_number)


# def _parse_motion_memory(line, line_number):
#     return StmtMotionMemory(source="", fps="")
#

class EventFormError(RuntimeError):
    pass


def _parse_unrecognized(line, line_number):
    return StmtUnrecognized(content=line, line_number=line_number)


def _parse_columns_for_standard_form(line: str, event_field_length: int,
                                     source_field_length: int,
                                     line_number: int):
    # breakpoint()
    col_widths = _edl_column_widths(event_field_length, source_field_length)

    if sum(col_widths) > len(line):
        raise EventFormError()

    column_strings = collimate(line, col_widths)

    channels = column_strings[4].strip()
    trans = column_strings[6].strip()

    if len(channels) == 0 or len(trans) == 0:
        raise EventFormError()

    return StmtEvent(event=column_strings[0],
                     source=column_strings[2].strip(),
                     channels=channels,
                     trans=trans,
                     trans_op=column_strings[8].strip(),
                     source_in=column_strings[10].strip(),
                     source_out=column_strings[12].strip(),
                     record_in=column_strings[14].strip(),
                     record_out=column_strings[16].strip(),
                     line_number=line_number,
                     source_field_size=source_field_length)


def _parse_columns_tolerant(line: str, line_number: int):
    pattern = re.compile(r'^\s*(\d+)\s+(.{8,128}?)\s+'
                         r'(V|A|A2|AA|NONE|AA/V|A2/V|B)\s+'
                         r'(C|D|W|KB|K|KO)\s+(\d*)\s+(\d\d.\d\d.\d\d.\d\d)\s'
                         r'(\d\d.\d\d.\d\d.\d\d)\s(\d\d.\d\d.\d\d.\d\d)\s'
                         r'(\d\d.\d\d.\d\d.\d\d)'
                         )

    match = pattern.match(line)
    if match:
        return StmtEvent(event=int(match.group(1)), source=match.group(2),
                         channels=match.group(3), trans=match.group(4),
                         trans_op=match.group(5), source_in=match.group(6),
                         source_out=match.group(7), record_in=match.group(8),
                         record_out=match.group(9), line_number=line_number,
                         source_field_size=len(match.group(2)))
    else:
        return StmtUnrecognized(line, line_number)


def _parse_source_umid_statement(line, line_number):
    # trimmed = line[3:].strip()
    # return StmtSourceUMID(name=None, umid=None, line_number=line_number)
    ...
