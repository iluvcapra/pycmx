# pycmx
# (c) 2018 Jamie Hardt

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

    chan_map = {     "V" :    (True,   False,   False),
                "A" :    (False,  True,    False),
                "A2" :   (False,  False,   True),
                "AA" :   (False,  True,    True),
                "B" :    (True,   True,    False),
                "V/AA" : (True,   True,    True),
                "V/A2" : (True,   False,   True)
        }


    def __init__(self, v=False, a1=False, a2=False, a3=False, a4=False):
        self.v = v
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.a4 = a4


    def appendEvent(self, event_str):
        if event_str in self.chan_map:
            channels = self.chan_map[event_str]
            self.v = channels[0]
            self.a1 = channels[1]
            self.a2 = channels[2]


    def appendExt(self, audio_ext):
        self.a3 = ext.audio3
        self.a4 = ext.audio4

    def __repr__(self):
        return "CmxChannelMap(v="+ self.v.__repr__( ) + \
                ",a1=" + self.a1.__repr__() + \
                ",a2=" + self.a2.__repr__() + \
                ",a3=" + self.a3.__repr__() + \
                ",a4=" + self.a4.__repr__() +")"
        
            
def parse_cmx3600(file):
    """Accepts the path to a CMX EDL and returns a list of all events contained therein."""
    statements = parse_cmx3600_statements(file)
    parser = NamedTupleParser(statements)
    parser.expect('Title')
    title = parser.current_token.title
    return event_list(title, parser)
    
def event_list(title, parser):
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
            channels = CmxChannelMap()
            channels.appendEvent(raw_event.channels)

            this_event = {'title': title, 'number': raw_event.event, 'clip_name': None ,
                                            'source_name': raw_event.source, 
                                            'channels': channels,
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
        elif parser.accept('Trailer'):
            break
        else:
            parser.next_token()
    
    if this_event != None:
        events_result.append(this_event)

    return events_result

