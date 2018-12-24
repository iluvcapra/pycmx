# pycmx
# (c) 2018 Jamie Hardt

from .parse_cmx_statements import (parse_cmx3600_statements, 
        StmtEvent, StmtFCM, StmtTitle, StmtClipName, StmtSourceFile, StmtAudioExt)

from collections import namedtuple

def parse_cmx3600(path):
    statements = parse_cmx3600_statements(path)
    return EditList(statements)
    
    
class EditList:
    def __init__(self, statements):
        self.title_statement = statements[0]
        self.event_statements = statements[1:]

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
    def source(self):
        return self.edit_statement.source

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

    

 

