# pycmx
# (c) 2018 Jamie Hardt

from .parse_cmx_statements import (parse_cmx3600_statements, 
        StmtEvent, StmtFCM, StmtTitle)

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

    def events(self):
        'Each event in the edit list'
        def events_p(statements_rest, curr_event_num, 
            statements_event, events, is_drop):

            stmt = statements_rest[0]
            rem  = statements_rest[1:]
                
            
            if type(stmt) is StmtEvent:
                if stmt.event == curr_event_num:
                    return ( rem,curr_event_num,statements_event + [stmt],events,is_drop)
                else:
                    new_event = Event(statements_event)
                    return ( rem,stmt.event, [stmt], events + [new_event],is_drop )
                    
            elif type(stmt) is StmtFCM:
                return ( rem, curr_event_num, statements_event, events,stmt.drop)
            else:
                return ( rem, curr_event_num, statements_event + [stmt],events, is_drop)

        
        result = (self.event_statements, None, [], [], False)
        while True:
            if len(result[0]) == 0:
                return result[3]
            else:
                result = events_p(*result)


class Event:
    def __init__(self, statements):
        self.statements = statements

    def number():
        return statements[0].event



