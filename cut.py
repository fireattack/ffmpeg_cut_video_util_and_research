
from django.utils.dateparse import parse_duration
import os
import subprocess
from pathlib import Path
import re
import datetime
import argparse

def ensure_name_nonexist(filename):
    i = 2
    stem = filename.stem
    while filename.exists():
        filename = filename.with_name(f'{stem}_{i}{filename.suffix}')
        i = i + 1
    return filename

def print_and_run(commands, confirm=False):
    confirm = confirm and not args.no_confirm
    commands_text_form = [f'"{c}"' if " " in str(c) else str(c) for c in commands]
    print('Commands is:')
    print(' '.join(commands_text_form))

    if not confirm or input('Do you want to start? Y/[N]').lower() == 'y':
        subprocess.run(commands)


def cut(p, inputs, flags, suffix):
    PRECUT = 5
    # set output filename
    if len(inputs) == 3 and inputs[2]:
        if inputs[2].split('.')[-1].lower() in ['mp4', 'mkv', 'ts']:
            p2 = Path(inputs[2])
        else:
            p2 = p.with_name(f'{p.stem} {inputs[2]} cut{suffix}')
    else:
        p2 = p.with_name(f'{p.stem} cut{suffix}')
    p2 = ensure_name_nonexist(p2)

    commands = ['ffmpeg', '-hide_banner']
    if suffix == '.ts':
        # https://superuser.com/questions/1609477/
        # Increase analyzeduration and probesize values so the second audio stream is analyzed.
        commands.extend(['-analyzeduration', '100M', '-probesize', '100M'])
    # don't add -ss if it's 0 to avoid messing up things with start time (not sure if it works though)
    if inputs[0] == 'start' or inputs[0] == '0':
        inputs[0] = '0'
        commands.extend(['-i', p])
    else:
        commands.extend(['-ss', inputs[0], '-i', p])
    if len(inputs) >= 2 and inputs[1] and inputs[1] != 'end':
        t = parse_duration(inputs[1]) - parse_duration(inputs[0])
        commands.extend(['-t', str(t)])
    else:
        t = None
    commands.extend(['-c', 'copy'])

    if not flags.get('doublecut') and not flags.get('forcenodouble'):
        # auto enable double cut if input is ts and -ss is greater than 5s and output is not ts
        if suffix.lower() == '.ts' and p2.suffix.lower() != '.ts' and parse_duration(inputs[0]).total_seconds() >= PRECUT:
            print(f'INFO: from TS to other formats, and -ss is greater than {PRECUT}s. Auto enabling double cut.')
            flags['doublecut'] = True

    if flags.get('doublecut') and not flags.get('forcenodouble'):
        if suffix.lower() != '.ts':
            print('WARN: It is recommended to only use double cut when input is ts.')
        if parse_duration(inputs[0]).total_seconds() < PRECUT:
            print(f'WARN: The start time is less than {PRECUT}s. Double cut is not possible.')
            return
        dummy_ss = parse_duration(inputs[0]) - datetime.timedelta(seconds=PRECUT)
        commands1 = ['ffmpeg', '-v', '0', '-ss', str(dummy_ss), '-i', p]
        if t:
            commands1.extend(['-t', str(t + datetime.timedelta(seconds=PRECUT))])
        # always precut to mp4 to avoid issues with mpegts
        temp = ensure_name_nonexist(Path(os.environ['TEMP']) / 'temp.mp4')
        commands1.extend(['-c', 'copy', '-map', '0:v', '-map', '0:a', temp])
        print_and_run(commands1)
        commands2 = ['ffmpeg', '-v', '0', '-ss', str(PRECUT), '-i', temp, '-c', 'copy', '-map', '0:v', '-map', '0:a']
        # avoid negative TS for mp4 to avoid edit list, for better compatibility
        if p2.suffix.lower() == '.mp4':
            commands2.extend(['-avoid_negative_ts', 'make_zero'])
        commands2.append(p2)
        print_and_run(commands2)

        temp.unlink()
        return

    # by default, ffmpeg copies first v/a tracks
    if flags.get('simple'):
        pass
        # commands.extend(['-map', '0:v:0', '-map', '0:a:0'])

    # Add some mapping, otherwise only the first v/a tracks are picked up.
    elif suffix.lower() == '.ts':
        # For TV recordings, there are often batch of bullshit streams like epg or subtitle streams.
        # it typically should be safe to copy if the output is also .ts
        if p2.suffix.lower() == '.ts':
            commands.extend(['-map', '0', '-copy_unknown']) # can add '-muxdelay', '0' to remove default 1.4s start time
        else:
            # drop all but video and audio streams for other formats because they don't really support other types
            commands.extend(['-map', '0:v', '-map', '0:a'])
            # avoid negative TS for mp4 to avoid edit list, for better compatibility
            if p2.suffix.lower() == '.mp4':
                commands.extend(['-avoid_negative_ts', 'make_zero'])
    else:
        # Copy all; may cause various problems with .TS. Try also flags like -ignore_unknown -copy_unknown -dn etc.
        commands.extend(['-map', '0'])
        # avoid negative TS for mp4 to avoid edit list, for better compatibility
        if p2.suffix.lower() == '.mp4':
            commands.extend(['-avoid_negative_ts', 'make_zero'])

    commands.append(p2)
    print_and_run(commands)

def main(p, inputs, flags):
    # set output suffix/format. The filename is set in cut()
    suffix = p.suffix
    if suffix == '.m2ts':
        suffix = '.ts'

    # if the inputs are already given, just run it.
    if inputs:
        cut(p, inputs, flags, suffix)
        return
    else:
        # interactive mode
        flags = {}
        while True:
            user_input = input('Please input timestamp (use \'help\' to see help; press enter to stop)\n')
            if user_input == 'help':
                print(
                    'Usage: [start] [end] [cut name or output filename]\n'
                    '  Example1: 00:04:00.23 01:01:00.100 cut1\n'
                    '  Example2: 00:00:00 end D:\mycut.mp4\n'
                    'You can also set or unset flag by using \'set <flag>\' or \'unset <flag>\'.\n'
                    'Available flag(s):\n'
                    '  simple: only the first audio/video stream is copied.\n'
                    '  doublecut: cut the video twice to make sure the start time for A/V is in sync. Useful for mpegts input. Will auto enable if it could help\n'
                    '  forcenodouble: force disable double cut.\n'
                )
            elif user_input.startswith('set '):
                flag = re.sub(r'^set ', '', user_input)
                flags[flag] = True
                print(f'Flag {flag} set.')
            elif user_input.startswith('unset '):
                flag = re.sub(r'^unset ', '', user_input)
                flags[flag] = False
                print(f'Flag {flag} unset.')
            elif user_input == '':
                break
            else:
                inputs = user_input.split(' ', 2)
                cut(p, inputs, flags, suffix)

        return

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("input", help="input file")
    parser.add_argument("commands", nargs='*', help="commands such as [start] [end] [cut name or output filename]; or leave empty to enter interactive mode")
    parser.add_argument("--simple", action='store_true', help="only the first audio/video stream is copied")
    parser.add_argument("--doublecut", action='store_true', help="when input is ts, cut the video twice to make sure the start time for A/V is in sync")
    parser.add_argument("--forcenodouble", action='store_true', help="force disable double cut")

    args = parser.parse_args()

    p = Path(args.input)
    assert p.exists(), f'{p} does not exist'
    flags = {}
    if args.simple:
        flags['simple'] = True
    if args.doublecut:
        flags['doublecut'] = True
    if args.forcenodouble:
        flags['forcenodouble'] = True
    main(p, args.commands, flags)