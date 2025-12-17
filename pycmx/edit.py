# pycmx
# (c) 2018-2025 Jamie Hardt

from .cdl import AscSopComponents, FramecountTriple
from .statements import (
    StmtCdlSat,
    StmtCdlSop,
    StmtFrmc,
    StmtEvent,
    StmtAudioExt,
    StmtClipName,
    StmtSourceFile,
    StmtEffectsName,
)
from .transition import Transition
from .channel_map import ChannelMap

from typing import Optional


class Edit:
    """
    An individual source-to-record operation, with a source roll, source and
    recorder timecode in and out, a transition and channels.
    """

    def __init__(
        self,
        edit_statement: StmtEvent,
        audio_ext_statement: Optional[StmtAudioExt],
        clip_name_statement: Optional[StmtClipName],
        source_file_statement: Optional[StmtSourceFile],
        trans_name_statement: Optional[StmtEffectsName] = None,
        asc_sop_statement: Optional[StmtCdlSop] = None,
        asc_sat_statement: Optional[StmtCdlSat] = None,
        frmc_statement: Optional[StmtFrmc] = None,
    ) -> None:
        # Assigning types for the attributes explicitly
        self._edit_statement: StmtEvent = edit_statement
        self._audio_ext: Optional[StmtAudioExt] = audio_ext_statement
        self._clip_name_statement: Optional[StmtClipName] = clip_name_statement
        self._source_file_statement: Optional[StmtSourceFile] = \
            source_file_statement
        self._trans_name_statement: Optional[StmtEffectsName] = \
            trans_name_statement
        self._asc_sop_statement: Optional[StmtCdlSop] = asc_sop_statement
        self._asc_sat_statement: Optional[StmtCdlSat] = asc_sat_statement
        self._frmc_statement: Optional[StmtFrmc] = frmc_statement

    @property
    def line_number(self) -> int:
        """
        Get the line number for the "standard form" statement associated with
        this edit. Line numbers a zero-indexed, such that the
        "TITLE:" record is line zero.
        """
        return self._edit_statement.line_number

    @property
    def channels(self) -> ChannelMap:
        """
        Get the :obj:`ChannelMap` object associated with this Edit.
        """
        cm = ChannelMap()
        cm._append_event(self._edit_statement.channels)
        if self._audio_ext is not None:
            cm._append_ext(self._audio_ext)
        return cm

    @property
    def transition(self) -> Transition:
        """
        Get the :obj:`Transition` that initiates this edit.
        """
        if self._trans_name_statement:
            return Transition(
                self._edit_statement.trans,
                self._edit_statement.trans_op,
                self._trans_name_statement.name,
            )
        else:
            return Transition(
                self._edit_statement.trans, self._edit_statement.trans_op, None
            )

    @property
    def source_in(self) -> str:
        """
        Get the source in timecode.
        """
        return self._edit_statement.source_in

    @property
    def source_out(self) -> str:
        """
        Get the source out timecode.
        """

        return self._edit_statement.source_out

    @property
    def record_in(self) -> str:
        """
        Get the record in timecode.
        """

        return self._edit_statement.record_in

    @property
    def record_out(self) -> str:
        """
        Get the record out timecode.
        """

        return self._edit_statement.record_out

    @property
    def source(self) -> str:
        """
        Get the source column. This is the 8, 32 or 128-character string on the
        event record line, this usually references the tape name of the source.
        """
        return self._edit_statement.source

    @property
    def black(self) -> bool:
        """
        The source field for thie edit was "BL". Black video or silence should
        be used as the source for this event.
        """
        return self.source == "BL"

    @property
    def aux_source(self) -> bool:
        """
        The source field for this edit was "AX". An auxiliary source is the
        source for this event.
        """
        return self.source == "AX"

    @property
    def source_file(self) -> Optional[str]:
        """
        Get the source file, as attested by a "* SOURCE FILE" remark on the
        EDL. This will return None if the information is not present.
        """
        if self._source_file_statement is None:
            return None
        else:
            return self._source_file_statement.filename

    @property
    def clip_name(self) -> Optional[str]:
        """
        Get the clip name, as attested by a "* FROM CLIP NAME" or "* TO CLIP
        NAME" remark on the EDL. This will return None if the information is
        not present.
        """
        if self._clip_name_statement is None:
            return None
        else:
            return self._clip_name_statement.name

    @property
    def asc_sop(self) -> Optional[AscSopComponents[float]]:
        """
        Get ASC CDL Slope-Offset-Power color transfer function for the edit,
        if present. The ASC SOP is a transfer function of the form:

        :math:`y = (ax + b)^p`

        for each color component the source, where the `slope` is `a`, `offset`
        is `b` and `power` is `p`.
        """
        if self._asc_sop_statement is None:
            return None

        return self._asc_sop_statement.cdl_sop

    @property
    def asc_sop_raw(self) -> Optional[str]:
        """
        ASC CDL Slope-Offset-Power statement raw line
        """
        if self._asc_sop_statement is None:
            return None

        return self._asc_sop_statement.line

    @property
    def asc_sat(self) -> Optional[float]:
        """
        Get ASC CDL saturation value for clip, if present
        """
        if self._asc_sat_statement is None:
            return None

        return self._asc_sat_statement.value

    @property
    def framecounts(self) -> Optional[FramecountTriple]:
        """
        Get frame count offset data, if it exists. If an FRMC statement exists
        in the EDL for the event it will give an integer frame count for the
        edit's source in and out times.
        """
        if not self._frmc_statement:
            return None

        return FramecountTriple(
            start=self._frmc_statement.start,
            end=self._frmc_statement.end,
            duration=self._frmc_statement.duration,
        )
