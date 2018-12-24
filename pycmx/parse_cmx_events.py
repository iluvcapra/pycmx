# pycmx
# (c) 2018 Jamie Hardt

from .parse_cmx_statements import (parse_cmx3600_statements, 
        StmtEvent, StmtFCM, StmtTitle, StmtClipName, StmtSourceFile, StmtAudioExt)

from .channel_map import ChannelMap

from collections import namedtuple

def parse_cmx3600(path):
    statements = parse_cmx3600_statements(path)
    return EditList(statements)
    
    
class EditList:
    def __init__(self, statements):
        self.title_statement = statements[0]
        self.event_statements = statements[1:]

    @property
    def title(self):
        'The title of the edit list'
        return self.title_statement.title

    @property
    def events(self):
        'A generator for all the events in the edit list'
        is_drop = None
        current_event_num = None
        event_statements = []
        for stmt in self.event_statements:
            if type(stmt) is StmtFCM:
                is_drop = stmt.drop
            elif type(stmt) is StmtEvent:
                if current_event_num is None:
                    current_event_num = stmt.event
                    event_statements.append(stmt)
                else:
                    if current_event_num != stmt.event:
                        yield Event(statements=event_statements)
                        event_statements = [stmt]
                        current_event_num = stmt.event
                    else:
                        event_statements.append(stmt)

            else:
                event_statements.append(stmt)

        yield Event(statements=event_statements)


class Edit:
    def __init__(self, edit_statement, audio_ext_statement, clip_name_statement, source_file_statement):
        self.edit_statement = edit_statement
        self.audio_ext = audio_ext_statement
        self.clip_name_statement = clip_name_statement
        self.source_file_statement = source_file_statement

    @property
    def channels(self):
        cm = ChannelMap()
        cm.append_event(self.edit_statement.channels)
        if self.audio_ext != None:
            cm.append_ext(self.audio_ext)
        return cm

    @property
    def transition(self):
        return Transition(self.edit_statement.trans, self.edit_statement.trans_op)
   
    @property
    def source_in(self):
        return self.edit_statement.source_in

    @property
    def source_out(self):
        return self.edit_statement.source_out

    @property
    def record_in(self):
        return self.edit_statement.record_in

    @property
    def record_out(self):
        return self.edit_statement.record_out

    @property
    def source(self):
        return self.edit_statement.source


    @property
    def source_file(self):
        return self.source_file_statement.filename


    @property
    def clip_name(self):
        if self.clip_name_statement != None:
            return self.clip_name_statement.name
        else:
            return None
        


class Event:
    def __init__(self, statements):
        self.statements = statements
    
    @property
    def number(self):
        return self._edit_statements()[0].event

    @property
    def edits(self):
        edits_audio = list( self._statements_with_audio_ext() )
        clip_names  = self._clip_name_statements()
        source_files= self._source_file_statements()
        
        the_zip = [edits_audio]

        if len(edits_audio) == 2:
            cn = [None, None]
            for clip_name in clip_names:
                if clip_name.affect == 'from':
                    cn[0] = clip_name
                elif clip_name.affect == 'to':
                    cn[1] = clip_name

            the_zip.append(cn)

        else:    
            if len(edits_audio) == len(clip_names):
                the_zip.append(clip_names)
            else:
                the_zip.append([None] * len(edits_audio) )

        if len(edits_audio) == len(source_files):
            the_zip.append(source_files)
        elif len(source_files) == 1:
            the_zip.append( source_files * len(edits_audio) )
        else:
            the_zip.append([None] * len(edits_audio) )


        return [ Edit(e1[0],e1[1],n1,s1) for (e1,n1,s1) in zip(*the_zip) ]
            
                

    def _edit_statements(self):
        return [s for s in self.statements if type(s) is StmtEvent]

    def _clip_name_statements(self):
        return [s for s in self.statements if type(s) is StmtClipName]
    
    def _source_file_statements(self):
        return [s for s in self.statements if type(s) is StmtSourceFile]
    
    def _statements_with_audio_ext(self):
        for (s1, s2) in zip(self.statements, self.statements[1:]):
            if type(s1) is StmtEvent and type(s2) is StmtAudioExt:
                yield (s1,s2)
            elif type(s1) is StmtEvent:
                yield (s1, None)

    

class Transition:
    """Represents a CMX transition, a wipe, dissolve or cut."""

    Cut = "C"
    Dissolve = "D"
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
    def cut(self):
        "`True` if this transition is a cut."
        return self.transition == 'C' 

    @property
    def dissolve(self):
        "`True` if this traansition is a dissolve."
        return self.transition == 'D'


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

