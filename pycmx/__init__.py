#!/usr/bin/env python
# coding: utf-8

# # CMX3600 EDL Parsing
# 
# ## String Helper
# 
# We start with a `colliate` function, which will help us divide a string into fixed-width columns.

# EDLs

def collimate(a_string, column_widths): 
    if len(column_widths) == 0:
        return []
    
    width = column_widths[0]
    element = a_string[:width]
    rest = a_string[width:]
    return [element] + collimate(rest, column_widths[1:]) 


# In[36]:


import re
import sys

from collections import namedtuple
import pprint 

pp = pprint.PrettyPrinter(depth=4)

#from itertools import repeat
#from functools import reduce


# ## Parsed Statement Data Structures
# 
# These represent individual lines that have been typed and have undergone some light symbolic parsing.



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


class NamedTupleParser:
    
    def __init__(self, tuple_list):
        self.tokens = tuple_list
        self.current_token = None
    
    def peek(self):
        return self.tokens[0]
    
    def at_end(self):
        return len(self.tokens) == 0
    
    def next_token(self):
        self.current_token = self.peek()
        self.tokens = self.tokens[1:]        
    
    def accept(self, type_name):
        if self.at_end(): 
            return False
        elif (type(self.peek()).__name__ == type_name ):
            self.next_token()
            return True
        else:
            return False
    
    def expect(self, type_name):
        assert( self.accept(type_name) )


class CmxChannelMap:
    def __init__(self, cmx_string):
        self.v = False
        self.a1 = False
        self.a2 = False
        self.a3 = False
        self.a4 = False
        if cmx_string == "V":
            self.v = True
        elif cmx_string == "A":
            self.a1 = True
        elif cmx_string == "A2":
            self.a2 = True
        elif cmx_string == "AA":
            self.a1 = True
            self.a2 = True
        elif cmx_string == "B":
            self.v = True
            self.a1 = True
        elif cmx_string == "V/AA":
            self.v = True
            self.a1 = True
            self.a2 = True
        elif cmx_string == "V/A2":
            self.v = True
            self.a2 = True
            
    def appendExt(self, audio_ext):
        self.a3 = ext.audio3
        self.a4 = ext.audio4
        
            

Cmx3600Event = namedtuple("Cmx3600Event",['title','number','clip_name', 'source_name','channels',
                                          'source_start','source_finish',
                                          'record_start','record_finish',
                                          'fcm_drop'])
    
def parse_cmx3600(file):
    statements = parse_cmx3600_statements(file)
    parser = NamedTupleParser(statements)
    parser.expect('Title')
    title = parser.current_token.title
    return event_list(title, parser)
    
def event_list(title, parser):
    print("Parsing event list")
    state = {"fcm_drop" : False}

    events_result = []
    this_event = None
    
    while not parser.at_end():
        if parser.accept('FCM'):
            state['fcm_drop'] = parser.current_token.drop
        elif parser.accept('Event'):
            if this_event != None:
                events_result.append(this_event)

            raw_event = parser.current_token
            this_event = {'title': title, 'number': raw_event.event, 'clip_name': None ,
                                            'source_name': raw_event.source, 
                                            'channels': CmxChannelMap(raw_event.channels),
                                            'source_start': raw_event.source_in,
                                            'source_finish': raw_event.source_out,
                                            'record_start': raw_event.record_in,
                                            'record_finish': raw_event.record_out,
                                            'fcm_drop': state['fcm_drop']}
        elif parser.accept('AudioExt'):
            this_event['channels'].appendExt(parser.current_token)
        elif parser.accept('ClipName'):
            this_event['clip_name'] = parser.current_token.name
        elif parser.accept('SourceFile'):
            this_event['source_name'] = parser.current_token.filename
        else:
            events_result.append(parser.current_token)
            parser.next_token()
    
    if this_event != None:
        events_result.append(this_event)

    return events_result

