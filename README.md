[![Build Status](https://travis-ci.com/iluvcapra/pycmx.svg?branch=master)](https://travis-ci.com/iluvcapra/pycmx)

# pycmx

The `pycmx` package provides a basic interface for parsing a CMX 3600 EDL and its most most common variations.

## Features

* The major variations of the CMX3600, the standard, "File32" and "File128" 
  formats are automatically detected and properly read.
* Preserves relationship between events and individual edits/clips.
* Remark or comment fields with common recognized forms are read and 
  available to the client, including clip name and source file data.
* Symbolically decodes transitions and audio channels.
* Does not parse or validate timecodes, does not enforce framerates, does not
  parameterize timecode or framerates in any way. This makes the parser more
  tolerant of EDLs with mixed rates.

## Usage

```
>>> import pycmx
>>> edl = pycmx.parse_cmx3600("tests/edls/TEST.edl")
>>> edl.title
'DC7 R1_v8.2'
>>> events = list( edl.events ) # the event list is a generator
>>> len(events)
120
>>> events[43].number 
'044'
>>> events[43].edits[0].source_in # events contain multiple 
                                  # edits to preserve A/B dissolves 
                                  # and key backgrounds
'00:00:00:00'
>>> events[43].edits[0].transition.cut
True
>>> events[43].edits[0].record_out
'01:10:21:10'
```

## Should I Use This?

At this time, this is (at best) alpha software and the interface will be 
changing often. It may be fun to experiment with but it is not suitable
at this time for production code.

Contributions are welcome and will make this module production-ready all the
faster! Please reach out or file a ticket! 
