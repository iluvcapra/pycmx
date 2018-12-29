# pycmx
# (c) 2018 Jamie Hardt

from .parse_cmx_statements import (StmtEvent, StmtClipName, StmtSourceFile, StmtAudioExt, StmtUnrecognized)
from .edit import Edit

class Event:
    """
    Represents a collection of :class:`Edit`s, all with the same event number.
    """

    def __init__(self, statements):
        self.statements = statements
    
    @property
    def number(self):
        """
        Return the event number.
        """
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

 
