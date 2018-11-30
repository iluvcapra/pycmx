
# Parsed Statement Data Structures
# 
# These represent individual lines that have been typed and have undergone some light symbolic parsing.

from .util import collimate
import re
import sys
from collections import namedtuple


StmtTitle = namedtuple("Title",["title"])
StmtFCM = namedtuple("FCM",["drop"])
StmtEvent = namedtuple("Event",["event","source","channels","trans","trans_op","source_in","source_out","record_in","record_out"])
StmtAudioExt = namedtuple("AudioExt",["audio3","audio4"])
StmtClipName = namedtuple("ClipName",["name"])
StmtSourceFile = namedtuple("SourceFile",["filename"])
StmtRemark = namedtuple("Remark",["text"])
StmtUnrecognized = namedtuple("Unrecognized",["content"])


def parse_cmx3600_statements(path):
    with open(path,'rU') as file:
        lines = file.readlines()
        return [parse_cmx3600_line(line.strip()) for line in lines]
    
def edl_column_widths(event_field_length, source_field_length):
    return [event_field_length,2, source_field_length,1,
                            4,2, # chans
                            4,1, # trans
                            3,1, # trans op
                            11,1,
                            11,1,
                            11,1,
                            11]
    
def parse_cmx3600_line(line):
    long_event_num_p  = re.compile("^[0-9]{6} ")
    short_event_num_p = re.compile("^[0-9]{3} ")
    
    if isinstance(line,str):
        if line.startswith("TITLE:"):
            return parse_title(line)
        elif line.startswith("FCM:"):
            return parse_fcm(line)
        elif long_event_num_p.match(line) != None:
            length_file_128 = sum(edl_column_widths(6,128))
            if len(line) < length_file_128:
                return parse_long_standard_form(line, 32)
            else:
                return parse_long_standard_form(line, 128)
        elif short_event_num_p.match(line) != None:
            return parse_standard_form(line)
        elif line.startswith("AUD"):
            return parse_extended_audio_channels(line)
        elif line.startswith("*"):
            return parse_remark( line[1:].strip())
        else:
            return parse_unrecognized(line)

    
def parse_title(line):
    title = line[6:].strip()
    return StmtTitle(title=title)

def parse_fcm(line):
    val = line[4:].strip()
    if val == "DROP FRAME":
        return StmtFCM(drop= True)
    else:
        return StmtFCM(drop= False)

def parse_long_standard_form(line,source_field_length):
    return parse_columns_for_standard_form(line, 6, source_field_length)
    
def parse_standard_form(line):
    return parse_columns_for_standard_form(line, 3, 8)
    
def parse_extended_audio_channels(line):
    content = line.strip()
    if content == "AUD   3":
        return StmtAudioExt(audio3=True, audio4=False)
    elif content == "AUD   4":
        return StmtAudioExt(audio3=False, audio4=True)
    elif content == "AUD   3     4":
        return StmtAudioExt(audio3=True, audio4=True)
    else:
        return StmtUnrecognized(content=line)
    
def parse_remark(line):
    if line.startswith("FROM CLIP NAME:"):
        return StmtClipName(name=line[15:].strip() )
    elif line.startswith("SOURCE FILE:"):
        return StmtSourceFile(filename=line[12:].strip() )
    else:
        return StmtRemark(text=line)

def parse_unrecognized(line):
    return StmtUnrecognized(content=line)

def parse_columns_for_standard_form(line, event_field_length, source_field_length):
    col_widths = edl_column_widths(event_field_length, source_field_length)
    
    if sum(col_widths) > len(line):
        return StmtUnrecognized(content=line)
    
    column_strings = collimate(line,col_widths)
        
    return StmtEvent(event=column_strings[0], 
                    source=column_strings[2].strip(), 
                    channels=column_strings[4].strip(),
                    trans=column_strings[6].strip(),
                     trans_op=column_strings[8].strip(),
                     source_in=column_strings[10].strip(),
                     source_out=column_strings[12].strip(),
                     record_in=column_strings[14].strip(),
                     record_out=column_strings[16].strip())


