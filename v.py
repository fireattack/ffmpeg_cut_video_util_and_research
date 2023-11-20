from subprocess import run
import json
from pathlib import Path
from rich import print as rprint


def dump_json(mydict, filename):
    filename = Path(filename)
    if filename.suffix.lower() !='.json':
        filename = filename.with_suffix('.json')
    filename.parent.mkdir(parents=True, exist_ok=True)
    with filename.open('w', encoding='utf-8') as f:
        json.dump(mydict, f, ensure_ascii=False, indent=2)


def extract_packets(video_path, mode='detailed', rezero=False, head=None):
    command = ['ffprobe', '-show_packets', '-print_format', 'json', video_path]
    result = run(command, capture_output=True)
    data = json.loads(result.stdout)
    dump_json(data, 'temp.json')

    packets = data['packets']
    if head:
        packets = packets[:head]

    print(f'Extracted {len(packets)} packets from {video_path}.')
    print(f'Video packets: {len([packet for packet in packets if packet["codec_type"] == "video"])}')
    print(f'Audio packets: {len([packet for packet in packets if packet["codec_type"] == "audio"])}')

    if mode == 'detailed':
        # grab all the TS values
        ts_values = [float(packet.get('pts_time', 0)) for packet in packets] + [float(packet.get('dts_time', 0)) for packet in packets]
        zero = 0
        if rezero:
            zero = min(ts_values)
            print(f'Re-zero: {zero} is the new zero.')
        # test min too because of negative values
        max_len = max(len(f'{max(ts_values):.3f}'), len(f'{min(ts_values):.3f}'))
        fmt = f'{max_len}.3f'

        for i, p in enumerate(packets):
            pts_time = float(p.get('pts_time', 0)) - zero
            dts_time = float(p.get('dts_time', 0)) - zero

            if p['codec_type'] == 'video':
                rprint(f"[green]V {pts_time:{fmt}} {dts_time:{fmt}} {p['flags']}[/green]", end='')
            elif p['codec_type'] == 'audio':
                rprint(f"[red]A {pts_time:{fmt}} {dts_time:{fmt}} {p['flags']}[/red]", end='')
            else:
                rprint(f"[blue]O {pts_time:{fmt}} {dts_time:{fmt}} {p['flags']}[/blue]", end='')
            if i % 8 == 7:
                print()
            else:
                print(' | ', end='')
        print()

    # another way to print packets
    if mode == 'simple':
        for i, p in enumerate(packets):
            if p['codec_type'] == 'video':
                rprint(f'[green]V[/green]', end='')
            elif p['codec_type'] == 'audio':
                rprint(f'[red]A[/red]', end='')
            # print a new line every 16 packets
            if i % 16 == 15:
                print()

    if mode == 'list':
        # print until at least 5 packets of each type are extracted
        count_a = 0
        count_v = 0
        for packet in packets:
            if packet['codec_type'] == 'audio':
                count_a += 1
            elif packet['codec_type'] == 'video':
                count_v += 1
            print(packet['codec_type'], packet['pts_time'], packet['flags'])
            if count_a >= 5 and count_v >= 5:
                break


def show_start_time(video_path, mute=False):
    command = ['ffprobe', '-show_packets', '-show_format', '-show_streams', '-print_format', 'json', video_path]
    result = run(command, capture_output=True)
    data = json.loads(result.stdout)

    dump_json(data, 'temp.json')
    format_start_time = float(data['format']['start_time'])
    not mute and print(f'Format start time: {format_start_time}')
    for stream in data['streams']:
        stream_type = stream['codec_type']
        stream_start_time = float(stream['start_time'])
        not mute and print(f'Stream {stream_type} start time: {stream_start_time}')
    packets = data['packets']
    video_packets = [packet for packet in packets if packet['codec_type'] == 'video']
    audio_packets = [packet for packet in packets if packet['codec_type'] == 'audio']

    not mute and print('Earliest video packet pts time:', min([float(packet['pts_time']) for packet in video_packets]))
    not mute and print('Earliest audio packet pts time:', min([float(packet['pts_time']) for packet in audio_packets]))

    not mute and print('Latest video packet pts time:', max([float(packet['pts_time']) for packet in video_packets]))
    not mute and print('Latest audio packet pts time:', max([float(packet['pts_time']) for packet in audio_packets]))

    return data

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['start', 's', 'packets', 'p'])
    parser.add_argument('video_path')
    parser.add_argument('--mode', choices=['detailed', 'simple', 'list'], default='detailed')
    parser.add_argument('--rezero', action='store_true')
    parser.add_argument('--head', type=int, help='only print the first N packets')

    args = parser.parse_args()
    if args.command in ['start', 's']:
        show_start_time(args.video_path)
    elif args.command in ['packets', 'p']:
        extract_packets(args.video_path, args.mode, args.rezero, args.head)
