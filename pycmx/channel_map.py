# pycmx
# (c) 2018 Jamie Hardt

from re import (compile, match)
from typing import Dict, Tuple, Generator

class ChannelMap:
    """
    Represents a set of all the channels to which an event applies.
    """

    _chan_map : Dict[str, Tuple] = {     
                "V" :    (True,   False,   False),
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
    def video(self) -> bool:
        'True if video is included'
        return self.v

    @property
    def audio(self) -> bool:
        'True if an audio channel is included'
        return len(self._audio_channel_set) > 0

    @property
    def channels(self) -> Generator[int, None, None]:
        'A generator for each audio channel'
        for c in self._audio_channel_set:
            yield c

    @property
    def a1(self) -> bool:
        """True if A1 is included"""
        return self.get_audio_channel(1)

    @a1.setter
    def a1(self, val: bool):
        self.set_audio_channel(1,val)

    @property
    def a2(self) -> bool:
        """True if A2 is included"""
        return self.get_audio_channel(2)

    @a2.setter
    def a2(self, val: bool):
        self.set_audio_channel(2,val)

    @property
    def a3(self) -> bool:
        """True if A3 is included"""
        return self.get_audio_channel(3)

    @a3.setter
    def a3(self, val: bool):
        self.set_audio_channel(3,val)
    
    @property
    def a4(self) -> bool:
        """True if A4 is included"""
        return self.get_audio_channel(4)

    @a4.setter
    def a4(self,val: bool):
        self.set_audio_channel(4,val)

    def get_audio_channel(self, chan_num) -> bool:
        """True if chan_num is included"""
        return (chan_num in self._audio_channel_set)

    def set_audio_channel(self,chan_num, enabled: bool):
        """If enabled is true, chan_num will be included"""
        if enabled:
            self._audio_channel_set.add(chan_num)
        elif self.get_audio_channel(chan_num):
            self._audio_channel_set.remove(chan_num)
    
    def _append_event(self, event_str):
        alt_channel_re = compile(r'^A(\d+)')
        if event_str in self._chan_map:
            channels = self._chan_map[event_str]
            self.v = channels[0]
            self.a1 = channels[1]
            self.a2 = channels[2]
        else:
            matchresult = match(alt_channel_re, event_str)
            if matchresult:
                self.set_audio_channel(int( matchresult.group(1)), True )

    def _append_ext(self, audio_ext):
        self.a3 = audio_ext.audio3
        self.a4 = audio_ext.audio4

    def __or__(self, other):
        """
        the logical union of this channel map with another
        """
        out_v = self.video | other.video
        out_a = self._audio_channel_set | other._audio_channel_set

        return ChannelMap(v=out_v,audio_channels = out_a)

