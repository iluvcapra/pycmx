# pycmx
# (c) 2018 Jamie Hardt

# Utility functions

def collimate(a_string, column_widths): 
    'Splits a string into substrings that are column_widths length.'
    
    if len(column_widths) == 0:
        return []
    
    width = column_widths[0]
    element = a_string[:width]
    rest = a_string[width:]
    return [element] + collimate(rest, column_widths[1:]) 


class NamedTupleParser:
    """
    Accepts a list of namedtuple and the client can step through the list with
    parser operations such as `accept()` and `expect()`
    """
    
    def __init__(self, tuple_list):
        self.tokens = tuple_list
        self.current_token = None
    
    def peek(self):
        """
        Returns the token to come after the `current_token` without
        popping the current token.
        """
        return self.tokens[0]
    
    def at_end(self):
        "`True` if the `current_token` is the last one."
        return len(self.tokens) == 0
    
    def next_token(self):
        "Sets `current_token` to the next token popped from the list"
        self.current_token = self.peek()
        self.tokens = self.tokens[1:]        
    
    def accept(self, type_name):
        """
        If the next token.__name__ is `type_name`, returns true and advances 
        to the next token with `next_token()`.
        """
        if self.at_end(): 
            return False
        elif (type(self.peek()).__name__ == type_name ):
            self.next_token()
            return True
        else:
            return False
    
    def expect(self, type_name):
        """
        If the next token.__name__ is `type_name`, the parser is advanced. 
        If it is not, an assertion failure occurs.
        """
        assert( self.accept(type_name) )


