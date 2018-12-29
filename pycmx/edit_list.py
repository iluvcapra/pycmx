# pycmx
# (c) 2018 Jamie Hardt

from .parse_cmx_statements import (StmtUnrecognized, StmtFCM, StmtEvent)
from .event import Event

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

