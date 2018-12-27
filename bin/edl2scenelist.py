import pycmx
import re
import argparse
import sys

def all_video_edits(edl):
    for event in edl.events:
        for edit in event.edits:
            if edit.channels.video:
                yield edit


def get_scene_name(edit, pattern):
    scene_extractor = re.compile(pattern, re.I)
    if edit.clip_name is None:
        return None
    else:
        match_data = re.match(scene_extractor, edit.clip_name)
        if match_data:
            return match_data[1]
        else:
            return edit.clip_name

def output_cmx(outfile, out_list):
    outfile.write("TITLE:  SCENE LIST\r\n")
    outfile.write("FCM: NON-DROP FRAME\r\n")

    for o in out_list:
        line = "%03i  AX       V     C        00:00:00:00 00:00:00:00 %s %s\r\n" % (0, o['start'],o['end'])
        outfile.write(line)
        outfile.write("* FROM CLIP NAME: %s\r\n" % (o['scene']) )

def output_cols(outfile, out_list):
    for o in out_list:
        outfile.write("%15s %15s %s\n" (o['start'], o['end'], o['scene'] )


def scene_list(infile, outfile, out_format, pattern):
    
    edl = pycmx.parse_cmx3600(infile)

    current_scene_name = None
    
    grouped_edits = [ ]

    for edit in all_video_edits(edl):
        this_scene_name = get_scene_name(edit, pattern)
        if this_scene_name is not None:
            if current_scene_name != this_scene_name:
                grouped_edits.append([ ])
                current_scene_name = this_scene_name

            grouped_edits[-1].append(edit)
    
    out_list = [ ]
    for group in grouped_edits:
        out_list.append({ 
            'start': group[0].record_in, 
            'end': group[-1].record_out,
            'scene': get_scene_name(group[0], pattern ) }
            )
    
    if out_format == 'cmx':
        output_cmx(outfile, out_list)
    elif out_format == 'cols':
        output_cols(outfile, out_list)


def scene_list_cli():
    parser = argparse.ArgumentParser(description=
            'Read video events from an input CMX EDL and output events merged into scenes.')
    parser.add_argument('-o','--outfile', default=sys.stdout, type=argparse.FileType('w'), 
            help='Output file. Default is stdout.')
    parser.add_argument('-f','--format', default='cmx', type=str, 
            help='Output format. Options are cols and cmx, cmx is the default.')
    parser.add_argument('-p','--pattern', default='V?([A-Z]*[0-9]+)',
            help='RE pattern for extracting scene name from clip name. The default is "V?([A-Z]*[0-9]+)". ' + \
                    'This pattern will be matched case-insensitively.')
    parser.add_argument('input_edl', default=sys.stdin, type=argparse.FileType('r'), nargs='?', 
            help='Input file. Default is stdin.')
    args = parser.parse_args()
    
    infile = args.input_edl

    scene_list(infile=infile, outfile=args.outfile , out_format=args.format, pattern=args.pattern)


if __name__ == '__main__':
   scene_list_cli()
