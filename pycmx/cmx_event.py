
class CmxEvent:
    """Represents a source-record event.

Aside from exposing properites related to the raw CMX event itself,
(the `source_start`, `source_finish`, `transition` etc.) the event
also contains contextual information from the parsed CMX list, such as 
`clip_name` and the frame counting mode in effect on the event.
    """
    
    def __init__(self,title,number,clip_name,source_name,channels, 
            transition,source_start,source_finish,
            record_start, record_finish, fcm_drop, remarks = [] , 
            unrecognized = [], line_number = None):
        self.title = title
        self.number = number
        self.clip_name = clip_name
        self.source_name = source_name
        self.channels = channels
        self.transition = transition
        self.source_start = source_start
        self.source_finish = source_finish
        self.record_start = record_start
        self.record_finish = record_finish
        self.fcm_drop = fcm_drop
        self.remarks = remarks
        self.unrecgonized = unrecognized
        self.black = (source_name == 'BL')
        self.aux_source = (source_name == 'AX')
        self.line_number = line_number


    def accept_statement(self, statement):
        """Used by the parser to attach clip names and notes to this event."""
        statement_type = type(statement).__name__ 
        if statement_type == 'AudioExt':
            self.channels.appendExt(statement)
        elif statement_type == 'Remark':
            self.remarks.append(statement.text)
        elif statement_type == 'SourceFile':
            self.source_name = statement.filename
        elif statement_type == 'ClipName':
            self.clip_name = statement.name
        elif statement_type == 'EffectsName':
            self.transition.name = statement.name
        
    def __repr__(self):
        return f"""CmxEvent(title={self.title.__repr__()},number={self.number.__repr__()},\
clip_name={self.clip_name.__repr__()},source_name={self.source_name.__repr__()},\
channels={self.channels.__repr__()},transition={self.transition.__repr__()},\
source_start={self.source_start.__repr__()},source_finish={self.source_finish.__repr__()},\
record_start={self.source_start.__repr__()},record_finish={self.record_finish.__repr__()},\
fcm_drop={self.fcm_drop.__repr__()},remarks={self.remarks.__repr__()},line_number={self.line_number.__repr__()})"""


class CmxTransition:
    """Represents a CMX transition, a wipe, dissolve or cut."""

    Cut = "C"
    Dissolve = "V"
    Wipe = "W"
    KeyBackground = "KB"
    Key = "K"
    KeyOut = "KO"

    def __init__(self, transition, operand):
        self.transition = transition
        self.operand = operand
        self.name = ''


    @property
    def kind(self):
        if self.cut:
            return Cut
        elif self.dissove:
            return Dissolve
        elif self.wipe:
            return Wipe
        elif self.key_background:
            return KeyBackground
        elif self.key_foreground:
            return Key
        elif self.key_out:
            return KeyOut

    @property
    def cut(self):
        "`True` if this transition is a cut."
        return self.transition == Cut 

    @property
    def dissolve(self):
        "`True` if this traansition is a dissolve."
        return self.transition == Dissolve


    @property
    def wipe(self):
        "`True` if this transition is a wipe."
        return self.transition.startswith('W')


    @property
    def effect_duration(self):
        """"`The duration of this transition, in frames of the record target.
        
        In the event of a key event, this is the duration of the fade in.
        """
        return int(self.operand)

    @property
    def wipe_number(self):
        "Wipes are identified by a particular number."
        if self.wipe:
            return int(self.transition[1:])
        else:
            return None

    @property
    def key_background(self):
        "`True` if this is a key background event."
        return self.transition == KeyBackground

    @property
    def key_foreground(self):
        "`True` if this is a key foreground event."
        return self.transition == Key

    @property
    def key_out(self):
        "`True` if this is a key out event."
        return self.transition == KeyOut

    def __repr__(self):
        return f"""CmxTransition(transition={self.transition.__repr__()},operand={self.operand.__repr__()})"""

