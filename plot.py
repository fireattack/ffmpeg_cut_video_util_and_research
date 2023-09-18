
from pathlib import Path
import matplotlib.pyplot as plt
from v import show_start_time


def plot(videos, title):
    count = len(videos)
    fig, axes = plt.subplots(count, 1, figsize=(10, count*1), layout="constrained", sharex=True)

    raw_data = show_start_time(videos[0], mute=True)
    video_ptss = [float(p['pts_time']) for p in raw_data['packets'] if p['codec_type'] == 'video']
    video_ptss.sort()
    OFFSET = video_ptss[-1] - video_ptss[0]

    for j, video in enumerate(videos):
        all_data = show_start_time(video, mute=True)
        ax = axes[j]
        ax.set_title(Path(video).name)

        if j != count - 1:
            ax.xaxis.set_visible(False)
            ax.spines[["left", "top", "right", "bottom"]].set_visible(False)
        else:
            ax.spines[["left", "top", "right"]].set_visible(False)
            # set x major ticks at 1 second interval
            ax.xaxis.set_major_locator(plt.MultipleLocator(1))

        # get offset
        video_ptss = [float(p['pts_time']) for p in all_data['packets'] if p['codec_type'] == 'video']
        video_ptss.sort()
        offset = video_ptss[-1] - OFFSET
        print(f'Offset is {offset}')

        # plot video packets
        data = [p for p in all_data['packets'] if p['codec_type'] == 'video']
        data.sort(key=lambda packet: float(packet['pts_time']))
        key_frame_count = len([p for p in data if p['flags'].startswith('K')])
        current_color = True if key_frame_count % 2 == 0 else False
        for i, d in enumerate(data):
            pts = float(d['pts_time'])
            pts -= offset
            duration = float(d['duration_time'])
            is_keyframe = d['flags'].startswith('K')
            if is_keyframe and not i == 0:
                current_color = not current_color
                print('Keyframe at {}'.format(pts))
            color = 'blue' if current_color else 'darkblue'
            if 'D' in d['flags']:
                color = 'red' if current_color else 'darkred'
            ax.barh('video', width=duration, left=pts, height=0.9, color=color)

        # plot audio packets
        data = [p for p in all_data['packets'] if p['codec_type'] == 'audio']
        data.sort(key=lambda packet: float(packet['pts_time']))

        current_color = True
        for i, d in enumerate(data):
            pts = float(d['pts_time'])
            pts -= offset
            duration = float(d['duration_time'])
            color = 'blue' if current_color else 'darkblue'
            if 'D' in d['flags']:
                color = 'red' if current_color else 'darkred'
            ax.barh('audio', width=duration, left=pts, height=0.9, color=color)
            current_color = not current_color

    fig.suptitle(title)
    plt.savefig(Rf'C:\files\ts_cut_bug\plot\{title}.png', pad_inches=0.1)


def main():
    plot(
        ['raw.ts', 'input_seeking_copy.ts', 'input_seeking_copy_tomkv.mkv', 'input_seeking_copy_tomp4.mp4', 'input_seeking_copy_tomp4_avoid_neg_ts.mp4'],
        'input seeking + copy')

    plot(['raw.ts', 'output_seeking_copy.ts', 'output_seeking_copy_tomkv.mkv', 'output_seeking_copy_tomp4.mp4'], 'output seeking + copy')

    plot(['raw.ts', 'fixmp4_input_seeking_copy.ts', 'fixmp4_input_seeking_copy_tomkv.mkv', 'fixmp4_input_seeking_copy_tomp4.mp4', 'fixmp4_input_seeking_copy_tomp4_avoid_neg_ts.mp4'],
        'fixmp4 + input seeking + copy')

    files = ['raw.mp4'] + list(Path.cwd().glob('diffss_inputseek_*.mkv'))
    plot(files, 'Various -ss when doing input seeking with fixmp4')

    files = ['raw.mp4'] + list(Path.cwd().glob('diffss_outputseek_*.mkv'))
    plot(files, 'Various -ss when doing output seeking with fixmp4')

    filenames = '''raw.ts
    intermediate.ts
    raw_to_interts_tots.ts
    raw_to_interts_tomp4.mp4
    intermediate.mp4
    raw_to_intermp4_tots.ts
    raw_to_intermp4_tomp4.mp4
    raw.mp4
    rawfixmp4_directly_tomp4.mp4
    rawfixmp4_directly_tots.ts'''

    files = [Path('test2') / l for l in filenames.splitlines()]
    plot(files, 'Pre-cut to intermediate (-ss 3), then cut to final (-ss 6)')


if __name__ == '__main__':
    # run all the batch files first.
    main()