from collections import namedtuple 

StmtTitle = namedtuple("Title", ["title", "line_number"])
StmtFCM = namedtuple("FCM", ["drop", "line_number"])
StmtEvent = namedtuple("Event", ["event", "source", "channels", "trans",
                                 "trans_op", "source_in", "source_out",
                                 "record_in", "record_out", "format",
                                 "line_number"])
StmtAudioExt = namedtuple("AudioExt", ["audio3", "audio4", "line_number"])
StmtClipName = namedtuple("ClipName", ["name", "affect", "line_number"])
StmtSourceFile = namedtuple("SourceFile", ["filename", "line_number"])
StmtCdlSop = namedtuple("CdlSop", ['slope_r','slope_g','slope_b', 
                                   'offset_r', 'offset_g', 'offset_b', 
                                   'power_r', 'power_g', 'power_b', 
                                   'line_number'])
StmtCdlSat = namedtuple("SdlSat", ['value'])
StmtRemark = namedtuple("Remark", ["text", "line_number"])
StmtEffectsName = namedtuple("EffectsName", ["name", "line_number"])
StmtSourceUMID = namedtuple("Source", ["name", "umid", "line_number"])
StmtSplitEdit = namedtuple("SplitEdit", ["video", "magnitude", "line_number"])
StmtMotionMemory = namedtuple(
    "MotionMemory", ["source", "fps"])  # FIXME needs more fields
StmtUnrecognized = namedtuple("Unrecognized", ["content", "line_number"])
