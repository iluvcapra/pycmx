# pycmx
# (c) 2018 Jamie Hardt

import re
import sys
from collections import namedtuple
from itertools import count
from typing import TextIO, List


from .util import collimate

StmtTitle =     namedtuple("Title",["title","line_number"])
StmtFCM =       namedtuple("FCM",["drop","line_number"])
StmtEvent =     namedtuple("Event",["event","source","channels","trans",\
        "trans_op","source_in","source_out","record_in","record_out","format","line_number"])
StmtAudioExt =  namedtuple("AudioExt",["audio3","audio4","line_number"])
StmtClipName =  namedtuple("ClipName",["name","affect","line_number"])
StmtSourceFile = namedtuple("SourceFile",["filename","line_number"])
StmtRemark =    namedtuple("Remark",["text","line_number"])
StmtEffectsName = namedtuple("EffectsName",["name","line_number"])
StmtSourceUMID =   namedtuple("Source",["name","umid","line_number"])
StmtSplitEdit = namedtuple("SplitEdit",["video","magnitude", "line_number"])
StmtMotionMemory = namedtuple("MotionMemory",["source","fps"]) # FIXME needs more fields
StmtUnrecognized = namedtuple("Unrecognized",["content","line_number"])


def parse_cmx3600_statements(file: TextIO) -> List[object]:
    """
    Return a list of every statement in the file argument.
    """
    lines = file.readlines()
    line_numbers = count() 
    return [_parse_cmx3600_line(line.strip(), line_number) \
            for (line, line_number) in zip(lines,line_numbers)]
    
def _edl_column_widths(event_field_length, source_field_length):
    return [event_field_length,2, source_field_length,1,
                            4,2, # chans
                            4,1, # trans
                            3,1, # trans op
                            11,1,
                            11,1,
                            11,1,
                            11]

def _edl_m2_column_widths():
    return [2, # "M2"
            3,3, #
            8,8,1,4,2,1,4,13,3,1,1]


def _parse_cmx3600_line(line, line_number):
    long_event_num_p  = re.compile("^[0-9]{6} ")
    short_event_num_p = re.compile("^[0-9]{3} ")
    
    if isinstance(line,str):
        if line.startswith("TITLE:"):
            return _parse_title(line,line_number)
        elif line.startswith("FCM:"):
            return _parse_fcm(line, line_number)
        elif long_event_num_p.match(line) != None:
            length_file_128 = sum(_edl_column_widths(6,128))
            if len(line) < length_file_128:
                return _parse_long_standard_form(line, 32, line_number)
            else:
                return _parse_long_standard_form(line, 128, line_number)
        elif short_event_num_p.match(line) != None:
            return _parse_standard_form(line, line_number)
        elif line.startswith("AUD"):
            return _parse_extended_audio_channels(line,line_number)
        elif line.startswith("*"):
            return _parse_remark( line[1:].strip(), line_number)
        elif line.startswith(">>> SOURCE"):
            return _parse_source_umid_statement(line, line_number)
        elif line.startswith("EFFECTS NAME IS"):
            return _parse_effects_name(line, line_number)
        elif line.startswith("SPLIT:"):
            return _parse_split(line, line_number)
        elif line.startswith("M2"):
            return _parse_motion_memory(line, line_number)
        else:
            return _parse_unrecognized(line, line_number)

    
def _parse_title(line, line_num):
    title = line[6:].strip()
    return StmtTitle(title=title,line_number=line_num)

def _parse_fcm(line, line_num):
    val = line[4:].strip()
    if val == "DROP FRAME":
        return StmtFCM(drop= True, line_number=line_num)
    else:
        return StmtFCM(drop= False, line_number=line_num)

def _parse_long_standard_form(line,source_field_length, line_number):
    return _parse_columns_for_standard_form(line, 6, source_field_length, line_number)
    
def _parse_standard_form(line, line_number):
    return _parse_columns_for_standard_form(line, 3, 8, line_number)
    
def _parse_extended_audio_channels(line, line_number):
    content = line.strip()
    if content == "AUD   3":
        return StmtAudioExt(audio3=True, audio4=False, line_number=line_number)
    elif content == "AUD   4":
        return StmtAudioExt(audio3=False, audio4=True, line_number=line_number)
    elif content == "AUD   3     4":
        return StmtAudioExt(audio3=True, audio4=True, line_number=line_number)
    else:
        return StmtUnrecognized(content=line, line_number=line_number)
    
def _parse_remark(line, line_number) -> object:
    if line.startswith("FROM CLIP NAME:"):
        return StmtClipName(name=line[15:].strip() , affect="from", line_number=line_number)
    elif line.startswith("TO CLIP NAME:"):
        return StmtClipName(name=line[13:].strip(), affect="to", line_number=line_number)
    elif line.startswith("SOURCE FILE:"):
        return StmtSourceFile(filename=line[12:].strip() , line_number=line_number)
    else:
        return StmtRemark(text=line, line_number=line_number)

def _parse_effects_name(line, line_number) -> StmtEffectsName:
    name = line[16:].strip()
    return StmtEffectsName(name=name, line_number=line_number)

def _parse_split(line, line_number):
    split_type = line[10:21]
    is_video = False
    if split_type.startswith("VIDEO"):
        is_video = True

    split_mag  = line[24:35]
    return StmtSplitEdit(video=is_video, magnitude=split_mag, line_number=line_number)


def _parse_motion_memory(line, line_number):
    return StmtMotionMemory(source = "", fps="")


def _parse_unrecognized(line, line_number):
    return StmtUnrecognized(content=line, line_number=line_number)

def _parse_columns_for_standard_form(line, event_field_length, source_field_length, line_number):
    col_widths = _edl_column_widths(event_field_length, source_field_length)
    
    if sum(col_widths) > len(line):
        return StmtUnrecognized(content=line, line_number=line_number)
    
    column_strings = collimate(line,col_widths)
        
    return StmtEvent(event=column_strings[0], 
                    source=column_strings[2].strip(), 
                    channels=column_strings[4].strip(),
                    trans=column_strings[6].strip(),
                     trans_op=column_strings[8].strip(),
                     source_in=column_strings[10].strip(),
                     source_out=column_strings[12].strip(),
                     record_in=column_strings[14].strip(),
                     record_out=column_strings[16].strip(),
		    line_number=line_number,
                    format=source_field_length)


def _parse_source_umid_statement(line, line_number):
    trimmed = line[3:].strip()
    return StmtSourceUMID(name=None, umid=None, line_number=line_number)

