[![Build Status](https://travis-ci.com/iluvcapra/pycmx.svg?branch=master)](https://travis-ci.com/iluvcapra/pycmx)

# pycmx

The `pycmx` package provides a basic interface for parsing a CMX 3600 EDL and its most most common variations.

## Features

* The major variations of the CMX3600, the standard, "File32" and "File128" 
  formats are automatically detected and properly read.
* Remark or comment fields with common recognized forms are read and 
  available to the client, including clip name and source file data.
* Symbolically decodes transitions

## Usage

```

>>> import pycmx
>>> result = pycmx.parse_cmx3600("STP R1 v082517.edl")
>>> print(result[0:3])
[CmxEvent(title='STP_Reel 1_082517',number=1,
    clip_name='FKI_LEADER_HEAD_1920X1080.MOV',
    source_name='FKI_LEADER_HEAD_1920X1080.MOV',
    channels=CmxChannelMap(v=True, audio_channels=set()),
    transition=CmxTransition(transition='C',operand=''),
    source_start='01:00:00:00',source_finish='01:00:08:00',
    record_start='01:00:00:00',record_finish='01:00:08:00',
    fcm_drop=False,remarks=[],line_number=2), 
CmxEvent(title='STP_Reel 1_082517',number=2,
    clip_name='BH_PRODUCTIONS_1.85_PRORES.MOV',
    source_name='BH_PRODUCTIONS_1.85_PRORES.MOV',
    channels=CmxChannelMap(v=True, audio_channels=set()),
    transition=CmxTransition(transition='C',operand=''),
    source_start='01:00:00:00',source_finish='01:00:14:23',
    record_start='01:00:00:00',record_finish='01:00:23:00',
    fcm_drop=False,remarks=[],line_number=5), 
CmxEvent(title='STP_Reel 1_082517',number=3,
    clip_name='V4L-1*',
    source_name='B116C001_150514_R0UR',
    channels=CmxChannelMap(v=True, audio_channels=set()),
    transition=CmxTransition(transition='C',operand=''),
    source_start='16:37:29:06',source_finish='16:37:40:22',
    record_start='16:37:29:06',record_finish='01:00:50:09',
    fcm_drop=False,remarks=[],line_number=8)]
```

## Known Issues/Roadmap

To be addressed:
* Does not decode "M2" speed changes.
* Does not decode repair notes, audio notes or other Avid-specific notes.
* Does not decode Avid marker list.

May not be addressed:

* Does not parse source list at end of EDL.

Probably beyond the scope of this module:
* Does not parse timecode entries.
* Does not parse color correction notes. For this functionality we refer you to [pycdl](https://pypi.org/project/pycdl/) or [cdl-convert](https://pypi.org/project/cdl-convert/).

## Should I Use This?

At this time, this is (at best) alpha software and the interface will be 
changing often. It may be fun to experiment with but it is not suitable
at this time for production code.

Contributions are welcome and will make this module production-ready all the
faster! Please reach out or file a ticket! 
