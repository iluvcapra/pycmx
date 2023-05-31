# pycmx
# (c) 2018 Jamie Hardt

from .parse_cmx_statements import (StmtUnrecognized, StmtFCM, StmtEvent, StmtSourceUMID)
from .event import Event
from .channel_map import ChannelMap

from typing import Generator

class EditList:
    """
    Represents an entire edit decision list as returned by :func:`~pycmx.parse_cmx3600()`.
    """
    def __init__(self, statements):
        self.title_statement = statements[0]
        self.event_statements = statements[1:]

    @property
    def format(self) -> str:
        """
        The detected format of the EDL. Possible values are: "3600", "File32",
        "File128", and "unknown".
        """
        first_event = next( (s for s in self.event_statements if type(s) is StmtEvent), None)

        if first_event:
            if first_event.format == 8:
                return '3600'
            elif first_event.format == 32:
                return 'File32'
            elif first_event.format == 128:
                return 'File128'
            else:
                return 'unknown'
        else:
            return 'unknown'
        

    @property
    def channels(self) -> ChannelMap:
        """
        Return the union of every channel channel.
        """

        retval = ChannelMap()
        for event in self.events:
            for edit in event.edits:
                retval = retval | edit.channels

        return retval
        

    @property
    def title(self) -> str:
        """
        The title of this edit list.
        """
        return self.title_statement.title

    
    @property
    def unrecognized_statements(self) -> Generator[StmtUnrecognized, None, None]:
        """
        A generator for all the unrecognized statements in the list.
        """
        for s in self.event_statements:
            if type(s) is StmtUnrecognized:
                yield s
        

    @property
    def events(self) -> Generator[Event, None, None]:
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

            elif type(stmt) is StmtSourceUMID:
                break
            else:
                event_statements.append(stmt)

        yield Event(statements=event_statements)

    @property
    def sources(self) -> Generator[StmtSourceUMID, None, None]:
        """
        A generator for all of the sources in the list
        """
        
        for stmt in self.event_statements:
            if type(stmt) is StmtSourceUMID:
                yield stmt


