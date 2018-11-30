# pycmx

The `pycmx` package provides a basic interface for parsing a CMX 3600 EDL and its most most common variations.

## Features

* The major variations of the CMX3600, the standard, "File32" and "File128" 
  formats are automatically detected and properly read.
* Remark or comment fields with common recognized forms are read and 
  available to the client, including clip name and source file data.

## Usage

```
import pycmx
pycmx.parse_cmx3600("INS4_R1_010417.edl") 
print(events[5:8])
>>> [CmxEvent(title='INS4_R1_010417', number='000006', 
       clip_name='V1A-6A', source_name='A192C008_160909_R1BY', 
       channels=CmxChannelMap(v=True,a1=False,a2=False,a3=False,a4=False), 
       source_start='19:26:38:13', source_finish='19:27:12:03', 
       record_start='01:00:57:15', record_finish='01:01:31:05', 
       fcm_drop=False), 
     CmxEvent(title='INS4_R1_010417', number='000007', 
        clip_name='1-4A', source_name='A188C004_160908_R1BY', 
        channels=CmxChannelMap(v=True,a1=False,a2=False,a3=False,a4=False), 
        source_start='19:29:48:01', source_finish='19:30:01:00', 
        record_start='01:01:31:05', record_finish='01:01:44:04', 
        fcm_drop=False), 
     CmxEvent(title='INS4_R1_010417', number='000008', 
        clip_name='2G-3', source_name='A056C007_160819_R1BY', 
        channels=CmxChannelMap(v=True,a1=False,a2=False,a3=False,a4=False), 
        source_start='19:56:27:14', source_finish='19:56:41:00', 
        record_start='01:01:44:04', record_finish='01:01:57:14', 
        fcm_drop=False)]
```

## Known Issues/Roadmap

To be addressed:
* Does not decode transitions.
* Does not decode "M2" speed changes.
* Does not decode repair notes, audio notes or other Avid-specific notes.

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
