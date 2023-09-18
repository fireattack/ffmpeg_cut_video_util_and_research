ffmpeg -v error -i raw.ts -c copy raw.mp4 -y
ffmpeg -v error -i raw.ts -c copy raw_fix.ts -y
ffmpeg -v error -i raw.ts -c copy raw_ffmpeg.mkv -y
mkvmerge raw.ts -o raw_mkvmerge.mkv

ffmpeg -v error -ss 00:00:03 -i raw_ffmpeg.mkv -c copy fixmkvffmpeg_input_seeking_copy.ts -y
ffmpeg -v error -ss 00:00:03 -i raw_ffmpeg.mkv -c copy fixmkvffmpeg_input_seeking_copy_tomp4.mp4 -y
ffmpeg -v error -ss 00:00:03 -i raw_ffmpeg.mkv -c copy fixmkvffmpeg_input_seeking_copy_tomkv.mkv -y

ffmpeg -v error -ss 00:00:03 -i raw_mkvmerge.mkv -c copy fixmkvmkvmerge_input_seeking_copy.ts -y
ffmpeg -v error -ss 00:00:03 -i raw_mkvmerge.mkv -c copy fixmkvmkvmerge_input_seeking_copy_tomp4.mp4 -y
ffmpeg -v error -ss 00:00:03 -i raw_mkvmerge.mkv -c copy fixmkvmkvmerge_input_seeking_copy_tomkv.mkv -y

ffmpeg -v error -ss 00:00:03 -i raw.mp4 -c copy fixmp4_input_seeking_copy.ts -y
ffmpeg -v error -ss 00:00:03 -i raw.mp4 -c copy fixmp4_input_seeking_copy_tomp4.mp4 -y
ffmpeg -v error -ss 00:00:03 -i raw.mp4 -c copy -avoid_negative_ts make_zero fixmp4_input_seeking_copy_tomp4_avoid_neg_ts.mp4 -y
ffmpeg -v error -ss 00:00:03 -i raw.mp4 -c copy fixmp4_input_seeking_copy_tomkv.mkv -y

ffmpeg -v error -ss 00:00:03 -i raw_fix.ts -c copy fixts_input_seeking_copy.ts -y
ffmpeg -v error -ss 00:00:03 -i raw_fix.ts -c copy fixts_ifixtsnput_seeking_copy_tomp4.mp4 -y
ffmpeg -v error -ss 00:00:03 -i raw_fix.ts -c copy -avoid_negative_ts make_zero fixts_input_seeking_copy_tomp4_avoid_neg_ts.mp4 -y
ffmpeg -v error -ss 00:00:03 -i raw_fix.ts -c copy fixts_input_seeking_copy_tomkv.mkv -y

ffmpeg -v error -ss 00:00:03 -i raw.mp4 -c:v libx264 -c:a aac fixmp4_input_seeking_encode.ts -y
ffmpeg -v error -ss 00:00:03 -i raw.mp4 -c:v libx264 -c:a aac fixmp4_input_seeking_encode_tomp4.mp4 -y
ffmpeg -v error -ss 00:00:03 -i raw.mp4 -c:v libx264 -c:a aac -avoid_negative_ts make_zero fixmp4_input_seeking_encode_tomp4_avoid_neg_ts.mp4 -y
ffmpeg -v error -ss 00:00:03 -i raw.mp4 -c:v libx264 -c:a aac fixmp4_input_seeking_encode_tomkv.mkv -y