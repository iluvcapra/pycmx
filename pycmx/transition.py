# pycmx
# (c) 2023 Jamie Hardt

from typing import Optional

class Transition:
    """
    A CMX transition: a wipe, dissolve or cut.
    """
    
    Cut = "C"
    Dissolve = "D"
    Wipe = "W"
    KeyBackground = "KB"
    Key = "K"
    KeyOut = "KO"

    def __init__(self, transition, operand, name=None):
        self.transition = transition
        self.operand = operand
        self.name = name

    @property
    def kind(self) -> Optional[str]:
        """
        Return the kind of transition: Cut, Wipe, etc
        """
        if self.cut:
            return Transition.Cut
        elif self.dissolve:
            return Transition.Dissolve
        elif self.wipe:
            return Transition.Wipe
        elif self.key_background:
            return Transition.KeyBackground
        elif self.key_foreground:
            return Transition.Key
        elif self.key_out:
            return Transition.KeyOut

    @property
    def cut(self) -> bool:
        "`True` if this transition is a cut."
        return self.transition == 'C' 

    @property
    def dissolve(self) -> bool:
        "`True` if this traansition is a dissolve."
        return self.transition == 'D'

    @property
    def wipe(self) -> bool:
        "`True` if this transition is a wipe."
        return self.transition.startswith('W')

    @property
    def effect_duration(self) -> int:
        """The duration of this transition, in frames of the record target.
        
        In the event of a key event, this is the duration of the fade in.
        """
        return int(self.operand)

    @property
    def wipe_number(self) -> Optional[int]:
        "Wipes are identified by a particular number."
        if self.wipe:
            return int(self.transition[1:])
        else:
            return None

    @property
    def key_background(self) -> bool:
        "`True` if this edit is a key background."
        return self.transition == Transition.KeyBackground

    @property
    def key_foreground(self) -> bool:
        "`True` if this edit is a key foreground."
        return self.transition == Transition.Key

    @property
    def key_out(self) -> bool:
        """
        `True` if this edit is a key out. This material will removed from
        the key foreground and replaced with the key background.
        """
        return self.transition == Transition.KeyOut


