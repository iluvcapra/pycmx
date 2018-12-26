# pycmx
# (c) 2018 Jamie Hardt

from .parse_cmx_statements import (parse_cmx3600_statements, 
        StmtEvent, StmtFCM, StmtTitle, StmtClipName, StmtSourceFile, StmtAudioExt, StmtUnrecognized)

from .channel_map import ChannelMap

from collections import namedtuple

def parse_cmx3600(f):
    """
    Parse a CMX 3600 EDL.

    Args:
        f : a file-like object, anything that's readlines-able.

    Returns:
        An :obj:`EditList`.
    """
    statements = parse_cmx3600_statements(f)
    return EditList(statements)
    
    
class EditList:
    """
    Represents an entire edit decision list as returned by `parse_cmx3600()`.
    
    """
    def __init__(self, statements):
        self.title_statement = statements[0]
        self.event_statements = statements[1:]

    @property
    def title(self):
        """
        The title of this edit list, as attensted by the 'TITLE:' statement on 
        the first line.
        """
        'The title of the edit list'
        return self.title_statement.title

    
    @property
    def unrecognized_statements(self):
        """
        A generator for all the unrecognized statements in the list.
        """
        for s in self.event_statements:
            if type(s) is StmtUnrecognized:
                yield s
        

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
    def __init__(self, edit_statement, audio_ext_statement, clip_name_statement, source_file_statement, other_statements = []):
        self.edit_statement = edit_statement
        self.audio_ext = audio_ext_statement
        self.clip_name_statement = clip_name_statement
        self.source_file_statement = source_file_statement
        self.other_statements = other_statements

    @property
    def line_number(self):
        """
        Get the line number for the "standard form" statement associated with
        this edit. Line numbers a zero-indexed, such that the 
        "TITLE:" record is line zero.
        """
        return self.edit_statement.line_number

    @property
    def channels(self):
        """
        Get the :obj:`ChannelMap` object associated with this Edit.
        """
        cm = ChannelMap()
        cm._append_event(self.edit_statement.channels)
        if self.audio_ext != None:
            cm._append_ext(self.audio_ext)
        return cm

    @property
    def transition(self):
        """
        Get the :obj:`Transition` object associated with this edit.
        """
        return Transition(self.edit_statement.trans, self.edit_statement.trans_op)
   
    @property
    def source_in(self):
        """
        Get the source in timecode.
        """
        return self.edit_statement.source_in

    @property
    def source_out(self):
        """
        Get the source out timecode.
        """

        return self.edit_statement.source_out

    @property
    def record_in(self):
        """
        Get the record in timecode.
        """

        return self.edit_statement.record_in

    @property
    def record_out(self):
        """
        Get the record out timecode.
        """

        return self.edit_statement.record_out

    @property
    def source(self):
        """
        Get the source column. This is the 8, 32 or 128-character string on the
        event record line, this usually references the tape name of the source.
        """
        return self.edit_statement.source


    @property
    def source_file(self):
        """
        Get the source file, as attested by a "* SOURCE FILE" remark on the
        EDL. This will return None if the information is not present.
        """
        if self.source_file_statement is None:
            return None
        else:
            return self.source_file_statement.filename


    @property
    def clip_name(self):
        """
        Get the clip name, as attested by a "* FROM CLIP NAME" or "* TO CLIP 
        NAME" remark on the EDL. This will return None if the information is
        not present.
        """
        if self.clip_name_statement != None:
            return self.clip_name_statement.name
        else:
            return None
        


class Event:
    """
    Represents a collection of :obj:`Edit`s, all with the same event number.
    """

    def __init__(self, statements):
        self.statements = statements
    
    @property
    def number(self):
        """Return the event number."""
        return int(self._edit_statements()[0].event)

    @property
    def edits(self):
        """
        Returns the edits. Most events will have a single edit, a single event
        will have multiple edits when a dissolve, wipe or key transition needs
        to be performed.
        """
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
            
    @property
    def unrecognized_statements(self):
        """
        A generator for all the unrecognized statements in the event.
        """
        for s in self.statements:
            if type(s) is StmtUnrecognized:
                yield s            

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
        """The duration of this transition, in frames of the record target.
        
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

