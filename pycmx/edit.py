# pycmx
# (c) 2018 Jamie Hardt

from .transition import Transition
from .channel_map import ChannelMap
# from .parse_cmx_statements import StmtEffectsName

from typing import Optional

class Edit:
    """
    An individual source-to-record operation, with a source roll, source and 
    recorder timecode in and out, a transition and channels.
    """
    def __init__(self, edit_statement, audio_ext_statement, clip_name_statement, source_file_statement, trans_name_statement = None):
        self.edit_statement = edit_statement
        self.audio_ext = audio_ext_statement
        self.clip_name_statement = clip_name_statement
        self.source_file_statement = source_file_statement
        self.trans_name_statement = trans_name_statement 

    @property
    def line_number(self) -> int:
        """
        Get the line number for the "standard form" statement associated with
        this edit. Line numbers a zero-indexed, such that the 
        "TITLE:" record is line zero.
        """
        return self.edit_statement.line_number

    @property
    def channels(self) -> ChannelMap:
        """
        Get the :obj:`ChannelMap` object associated with this Edit.
        """
        cm = ChannelMap()
        cm._append_event(self.edit_statement.channels)
        if self.audio_ext != None:
            cm._append_ext(self.audio_ext)
        return cm

    @property
    def transition(self) -> Transition:
        """
        Get the :obj:`Transition` object associated with this edit.
        """
        if self.trans_name_statement:
            return Transition(self.edit_statement.trans, self.edit_statement.trans_op, self.trans_name_statement.name)
        else:
            return Transition(self.edit_statement.trans, self.edit_statement.trans_op, None)
    
    @property
    def source_in(self) -> str:
        """
        Get the source in timecode.
        """
        return self.edit_statement.source_in

    @property
    def source_out(self) -> str:
        """
        Get the source out timecode.
        """

        return self.edit_statement.source_out

    @property
    def record_in(self) -> str:
        """
        Get the record in timecode.
        """

        return self.edit_statement.record_in

    @property
    def record_out(self) -> str:
        """
        Get the record out timecode.
        """

        return self.edit_statement.record_out

    @property
    def source(self) -> str:
        """
        Get the source column. This is the 8, 32 or 128-character string on the
        event record line, this usually references the tape name of the source.
        """
        return self.edit_statement.source

    @property
    def black(self) -> bool:
        """
        Black video or silence should be used as the source for this event.
        """
        return self.source == "BL"

    @property
    def aux_source(self) -> bool:
        """
        An auxiliary source is the source of this event.
        """
        return self.source == "AX"

    @property
    def source_file(self) -> Optional[str]:
        """
        Get the source file, as attested by a "* SOURCE FILE" remark on the
        EDL. This will return None if the information is not present.
        """
        if self.source_file_statement is None:
            return None
        else:
            return self.source_file_statement.filename

    @property
    def clip_name(self) -> Optional[str]:
        """
        Get the clip name, as attested by a "* FROM CLIP NAME" or "* TO CLIP 
        NAME" remark on the EDL. This will return None if the information is
        not present.
        """
        if self.clip_name_statement is None:
            return None
        else:
            return self.clip_name_statement.name


