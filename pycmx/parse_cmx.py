#!/usr/bin/env python
# coding: utf-8

# # CMX3600 EDL Parsing
# 
# ## String Helper
# 
# We start with a `colliate` function, which will help us divide a string into fixed-width columns.

# EDLs

from .parse_cmx_statements import parse_cmx3600_statements
from collections import namedtuple

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
    """Accepts the path to a CMX EDL and returns a list of all events contained therein."""
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

