.. pycmx documentation master file, created by
   sphinx-quickstart on Wed Dec 26 21:51:43 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pycmx -  A CMX EDL Parser in Python
====================================

The `pycmx` package parses a CMX 3600 EDL and its most most common variations.

Features
---------

* The major variations of the CMX 3600: the standard, "File32", "File128" and
  long Adobe Premiere event numbers are automatically detected and properly
  read. Event number field and source name field sizes are determined
  dynamically for each statement for a high level of compliance at the expense
  of strictness.
* Preserves relationship between events and individual edits/clips.
* Remark or comment fields with common recognized forms are read and 
  available to the client, including clip name and source file data.
* ASC SOP, Saturation and FRMC statements are parsed and decoded.
* Symbolically decodes transitions and audio channels.
* Does not parse or validate timecodes, does not enforce framerates, does not
  parameterize timecode or framerates in any way. This makes the parser more
  tolerant of EDLs with mixed rates.
* Unrecognized lines are accessible on the `EditList` and `Event` classes
  along with the line numbers, to help the client diagnose problems with a
  list and give the client the ability to extend the package with their own
  parsing code.


.. toctree::
   :maxdepth: 5
   :caption: API Reference

   function
   classes

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
