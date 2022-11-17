[![Documentation Status](https://readthedocs.org/projects/pycmx/badge/?version=latest)](https://pycmx.readthedocs.io/en/latest/?badge=latest) ![](https://img.shields.io/github/license/iluvcapra/pycmx.svg) ![](https://img.shields.io/pypi/pyversions/pycmx.svg) [![](https://img.shields.io/pypi/v/pycmx.svg)](https://pypi.org/project/pycmx/) ![](https://img.shields.io/pypi/wheel/pycmx.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/iluvcapra/pycmx)
[![Lint and Test](https://github.com/iluvcapra/pycmx/actions/workflows/python-package.yml/badge.svg)](https://github.com/iluvcapra/pycmx/actions/workflows/python-package.yml)


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


