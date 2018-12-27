[![Build Status](https://travis-ci.com/iluvcapra/pycmx.svg?branch=master)](https://travis-ci.com/iluvcapra/pycmx) [![Documentation Status](https://readthedocs.org/projects/pycmx/badge/?version=latest)](https://pycmx.readthedocs.io/en/latest/?badge=latest)


# pycmx

The `pycmx` package provides a basic interface for parsing a CMX 3600 EDL and its most most common variations.

## Features

* The major variations of the CMX 3600: the standard, "File32" and "File128" 
  formats are automatically detected and properly read.
* Preserves relationship between events and individual edits/clips.
* Remark or comment fields with common recognized forms are read and 
  available to the client, including clip name and source file data.
* Symbolically decodes transitions and audio channels.
* Does not parse or validate timecodes, does not enforce framerates, does not
  parameterize timecode or framerates in any way. This makes the parser more
  tolerant of EDLs with mixed rates.
* Unrecognized lines are accessible on the `EditList` and `Event` classes
  along with the line numbers, to help the client diagnose problems with a
  list and give the client the ability to extend the package with their own
  parsing code.

## Usage

### Opening and Parsing EDL Files
```
>>> import pycmx
>>> with open("tests/edls/TEST.edl") as f
... 	edl = pycmx.parse_cmx3600(f)
...
>>> edl.title
'DC7 R1_v8.2'
```

### Reading Events and Edits

`EditList.events` is a generator...

```
>>> events = list( edl.events )  
>>> len(events)
120
>>> events[43].number 
'044'
```

...and events contain 1...n edits.

```
>>> events[43].edits[0].source_in 
'00:00:00:00'
>>> events[43].edits[0].transition.cut
True
>>> events[43].edits[0].record_out
'01:10:21:10'
```

### Acessing Transitions and Enabled Channels

```           
>>> events[41].edits[0].transition.dissolve
False
>>> events[41].edits[1].transition.dissolve
True
>>> events[41].edits[0].clip_name
'TC R1 V1.2 TEMP1 DX M.WAV'
>>> events[41].edits[1].clip_name
'TC R1 V6 TEMP2 M DX.WAV'
   
              # parsed channel maps are also
              # available to the client
>>> events[2].edits[0].channels.get_audio_channel(7)
True
>>> events[2].edits[0].channels.get_audio_channel(6)
False
>>> for c in events[2].edits[0].channels.channels:
...     print(f"Audio channel {c} is present")
... 
Audio channel 7 is present
>>> events[2].edits[0].channels.video
False
```

## How is this different from `python-edl`?

There are two important differences between `import edl` and `import pycmx` 
and motivated my development of this module.

1. The `pycmx` parser doesn't take timecode or framerates into account, 
   and strictly treats timecodes like opaque values. As far as `pycmx` is 
   concerend, they're just strings. This was done because in my experience, 
   the frame rate of an EDL is often difficult to precisely determine and 
   often the frame rate of various sources is different from the frame rate 
   of the target track.
   
   In any event, timecodes in an EDL are a kind of *address* and are not
   exactly scalar, they're meant to point to a particular block of video or 
   audio data on a medium and presuming that they refer to a real time, or 
   duration, or are convertible, etc. isn't always safe.

2. The `pycmx` parser reads event numbers and keeps track of which EDL rows
   are meant to happen "at the same time," with two decks. This makes it 
   easier to reconstruct transition A/B clips, and read clip names from
   such events appropriately.
 
## Should I Use This?

At this time, this is (at best) beta software. I feel like the interface is 
about where where I'd like it to be but more testing is required.

Contributions are welcome and will make this module production-ready all the
faster! Please reach out or file a ticket! 
