# pycmx
# (c) 2018 Jamie Hardt

# Utility functions

def collimate(a_string, column_widths): 
    """
    Split a list-type thing, like a string, into slices that are column_widths 
    length.
    
    >>> collimate("a b1 c2345",[2,3,3,2])
    ['a ','b1 ','c23','45']

    Args:
        a_string: The string to split. This parameter can actually be anything
            sliceable.
        column_widths: A list of integers, each one is the length of a column. 

    Returns:
        A list of slices. The len() of the returned list will *always* equal 
        len(:column_widths:). 
    """
    
    if len(column_widths) == 0:
        return []
    
    width = column_widths[0]
    element = a_string[:width]
    rest = a_string[width:]
    return [element] + collimate(rest, column_widths[1:]) 

