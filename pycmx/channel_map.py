# pycmx
# (c) 2018 Jamie Hardt

from re import (compile, match)

class ChannelMap:

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
    def video(self):
        'True if video is included'
        return self.v

    @property
    def channels(self):
        'A generator for each audio channel'
        for c in self._audio_channel_set:
            yield c

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
    
    def append_event(self, event_str):
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

    def append_sxt(self, audio_ext):
        self.a3 = ext.audio3
        self.a4 = ext.audio4

