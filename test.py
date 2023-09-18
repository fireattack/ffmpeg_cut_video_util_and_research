from util import load_json
from v import show_start_time
from pathlib import Path

for f in Path.cwd().iterdir():
    if (f.name.startswith('fix') or f.name.startswith('raw')) and f.suffix not in ['.bat', '.json']:
        print(f.name)
        data = show_start_time(f, mute=True)
        for p in data['packets']:
            if p['codec_type'] == 'video' and p["flags"].startswith('K'):
                print(p['size'], end=' ')
        print()
