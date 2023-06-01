# pycmx
# (c) 2023 Jamie Hardt

from .parse_cmx_statements import (StmtEvent, StmtClipName, StmtSourceFile, StmtAudioExt, StmtUnrecognized, StmtEffectsName)
from .edit import Edit 

from typing import List, Generator, Optional, Tuple, Any

class Event:
    """
    Represents a collection of :class:`~pycmx.edit.Edit` s, all with the same event number.
    """

    def __init__(self, statements):
        self.statements = statements
    
    @property
    def number(self) -> int:
        """
        Return the event number.
        """
        return int(self._edit_statements()[0].event)

    @property
    def edits(self) -> List[Edit]:
        """
        Returns the edits. Most events will have a single edit, a single event
        will have multiple edits when a dissolve, wipe or key transition needs
        to be performed.
        """
        edits_audio = list( self._statements_with_audio_ext() )
        clip_names  = self._clip_name_statements()
        source_files= self._source_file_statements()
         
        the_zip: List[List[Any]] = [edits_audio]

        if len(edits_audio) == 2:
            start_name: Optional[StmtClipName] = None
            end_name: Optional[StmtClipName] = None

            for clip_name in clip_names:
                if clip_name.affect == 'from':
                    start_name = clip_name
                elif clip_name.affect == 'to':
                    end_name = clip_name

            the_zip.append([start_name, end_name])
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
        
        # attach trans name to last event
        try:
            trans_statement = self._trans_name_statements()[0]
            trans_names: List[Optional[Any]] = [None] * (len(edits_audio) - 1)
            trans_names.append(trans_statement)
            the_zip.append(trans_names)
        except IndexError:
            the_zip.append([None] * len(edits_audio) )

        return [ Edit(edit_statement=e1[0],
                      audio_ext_statement=e1[1],
                      clip_name_statement=n1,
                      source_file_statement=s1,
                      trans_name_statement=u1) for (e1,n1,s1,u1) in zip(*the_zip) ]
            
    @property
    def unrecognized_statements(self) -> Generator[StmtUnrecognized, None, None]:
        """
        A generator for all the unrecognized statements in the event.
        """
        for s in self.statements:
            if type(s) is StmtUnrecognized:
                yield s
    
    def _trans_name_statements(self) -> List[StmtEffectsName]:
        return [s for s in self.statements if type(s) is StmtEffectsName]

    def _edit_statements(self) -> List[StmtEvent]:
        return [s for s in self.statements if type(s) is StmtEvent]

    def _clip_name_statements(self) -> List[StmtClipName]:
        return [s for s in self.statements if type(s) is StmtClipName]
    
    def _source_file_statements(self) -> List[StmtSourceFile]:
        return [s for s in self.statements if type(s) is StmtSourceFile]
    
    def _statements_with_audio_ext(self) -> Generator[Tuple[StmtEvent, Optional[StmtAudioExt]], None, None]:
        for (s1, s2) in zip(self.statements, self.statements[1:]):
            if type(s1) is StmtEvent and type(s2) is StmtAudioExt:
                yield (s1,s2)
            elif type(s1) is StmtEvent:
                yield (s1, None)

 
