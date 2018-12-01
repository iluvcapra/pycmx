class CmxEvent:
    def __init__(self,title,number,clip_name,source_name,channels, 
            transition,source_start,source_finish,
            record_start, record_finish, fcm_drop, remarks = [] , 
            unrecognized = []):
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


    def accept_statement(statement):
        atement_type = type(statement).__name__ 
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
        return f"""CmxEvent(title="{self.title}",number="{self.number}",\
clip_name="{self.clip_name}",source_name="{self.source_name}",\
channels={self.channels},transition={self.transition},\
source_start="{self.source_start}",source_finish="{self.source_finish}",\
record_start="{self.source_start}",record_finish="{self.record_finish}",\
fcm_drop={self.fcm_drop},remarks={self.remarks})"""


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
        return f"""CmxTransition(transition="{self.transition}",operand="{self.operand}")"""

