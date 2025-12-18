.. pycmx documentation master file, created by
   sphinx-quickstart on Wed Dec 26 21:51:43 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pycmx -  A CMX EDL Parser in Python
====================================

Features
---------

The `pycmx` package parses a CMX 3600 EDL and its most most common variations.

* The major variations of the CMX 3600: the standard, "File32", "File128" and
  long Adobe Premiere event numbers are automatically detected and properly
  read. Event number field and source name field sizes are determined
  dynamically for each statement for a high level of compliance at the expense
  of strictness.
* An more relaxed "tolerant" mode allows parsing of an EDL file where columns
  use non-standard widths.
* Preserves relationship between events and individual edits/clips.
* Remark or comment fields with common recognized forms are read and 
  available to the client, including clip name and source file data.
* `ASC CDL`_ and FRMC statements are parsed and decoded.
* Symbolically decodes transitions and audio channels.
* Does not parse or validate timecodes, does not enforce framerates, does not
  parameterize timecode or framerates in any way. This makes the parser more
  tolerant of EDLs with mixed rates.
* Unrecognized lines are accessible on the `EditList` and `Event` classes
  along with the line numbers, to help the client diagnose problems with a
  list and give the client the ability to extend the package with their own
  parsing code.

.. _ASC CDL: https://en.wikipedia.org/wiki/ASC_CDL

Getting Started
----------------

Install `pycmx` with pip, or add it with `uv` or your favorite tool.

.. code-block:: sh

   pip install pycmx

`pycmx` parses an EDL with the :func:`~pycmx.parse_cmx_events.parse_cmx3600`
function:

.. code-block:: python
   
  import pycmx
   
  with open("tests/edls/TEST.edl") as f:
    edl = pycmx.parse_cmx3600(f)

The `pycmx` parser reads each line from the input EDL and collects them into
`~pycmx.event.Event` objects. All individual edit actions that share the same
event number will be collected into a single Event, along with transitions and
any remark lines, including clip names, and CDL color commands.

.. code-block:: python

  for event in edl.events:
    print("- - - Event Info - - -")
    print("Event No:", event.number)
    for edit in event.edits:
      print("On Line No:", edit.line_number)
      print("Transition In:", edit.transition.kind)
      print("Source Name:", edit.source)
      print("Source In:", edit.source_in)
      print("Source Out:", edit.source_out)
      print("Rec In:", edit.record_in)
      print("Rec Out:", edit.record_out)
      print("ASC SOP:", edit.asc_sop)


.. toctree::
   :maxdepth: 5
   :caption: API Reference

   function
   classes

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
