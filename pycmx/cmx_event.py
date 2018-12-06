class CmxEvent:
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


    def can_accept(self):
        return {'AudioExt','Remark','SourceFile','ClipName','EffectsName'}

    def accept_statement(self, statement):
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
    def __init__(self, transition, operand):
        self.transition = transition
        self.operand = operand
        self.name = ''

    @property
    def cut(self):
        return self.transition == 'C'

    @property
    def dissolve(self):
        return self.transition == 'D'


    @property
    def wipe(self):
        return self.transition.startswith('W')


    @property
    def effect_duration(self):
        return int(self.operand)

    @property
    def wipe_number(self):
        if self.wipe:
            return int(self.transition[1:])
        else:
            return None

    @property
    def key_background(self):
        return self.transition == 'KB'

    @property
    def key_foreground(self):
        return self.transition == 'K'

    @property
    def key_out(self):
        return self.transition == 'KO'

    def __repr__(self):
        return f"""CmxTransition(transition={self.transition.__repr__()},operand={self.operand.__repr__()})"""

