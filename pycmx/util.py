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


