# pycmx
# (c) 2018 Jamie Hardt

from .parse_cmx_statements import parse_cmx3600_statements
from .cmx_event import CmxEvent, CmxTransition
from collections import namedtuple

from re import compile, match

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
    """
    Represents a set of all the channels to which an event applies.
    """

    chan_map = {     "V" :    (True,   False,   False),
                "A" :    (False,  True,    False),
                "A2" :   (False,  False,   True),
                "AA" :   (False,  True,    True),
                "B" :    (True,   True,    False),
                "AA/V" : (True,   True,    True),
                "A2/V" : (True,   False,   True)
        }


    def __init__(self, v=False, audio_channels=set()):
        self._audio_channel_set = audio_channels 
        self.v = v

    @property
    def a1(self):
        return self.get_audio_channel(1)

    @a1.setter
    def a1(self,val):
        self.set_audio_channel(1,val)

    @property
    def a2(self):
        return self.get_audio_channel(2)

    @a2.setter
    def a2(self,val):
        self.set_audio_channel(2,val)

    @property
    def a3(self):
        return self.get_audio_channel(3)

    @a3.setter
    def a3(self,val):
        self.set_audio_channel(3,val)
    
    @property
    def a4(self):
        return self.get_audio_channel(4)

    @a4.setter
    def a4(self,val):
        self.set_audio_channel(4,val)


    def get_audio_channel(self,chan_num):
        return (chan_num in self._audio_channel_set)

    def set_audio_channel(self,chan_num,enabled):
        if enabled:
            self._audio_channel_set.add(chan_num)
        elif self.get_audio_channel(chan_num):
            self._audio_channel_set.remove(chan_num)
            

    def appendEvent(self, event_str):
        alt_channel_re = compile('^A(\d+)')
        if event_str in self.chan_map:
            channels = self.chan_map[event_str]
            self.v = channels[0]
            self.a1 = channels[1]
            self.a2 = channels[2]
        else:
            matchresult = match(alt_channel_re, event_str)
            if matchresult:
                self.set_audio_channel(int( matchresult.group(1)), True )

    def appendExt(self, audio_ext):
        self.a3 = ext.audio3
        self.a4 = ext.audio4

    def __repr__(self):
        return f"CmxChannelMap(v={self.v.__repr__()}, audio_channels={self._audio_channel_set.__repr__()})"
        
            
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
            channels = CmxChannelMap(v=False, audio_channels=set([]))
            channels.appendEvent(raw_event.channels)

            this_event = CmxEvent(title=title,number=int(raw_event.event), clip_name=None ,
                                            source_name=raw_event.source, 
                                            channels=channels,
                                            transition=CmxTransition(raw_event.trans, raw_event.trans_op),
                                            source_start= raw_event.source_in,
                                            source_finish= raw_event.source_out,
                                            record_start= raw_event.record_in,
                                            record_finish= raw_event.record_out,
                                            fcm_drop= state['fcm_drop'],
					    line_number = raw_event.line_number)
        elif parser.accept('AudioExt') or parser.accept('ClipName') or \
        parser.accept('SourceFile') or parser.accept('EffectsName') or \
        parser.accept('Remark'):
            this_event.accept_statement(parser.current_token)
        elif parser.accept('Trailer'):
            break
        else:
            parser.next_token()
    
    if this_event != None:
        events_result.append(this_event)

    return events_result

