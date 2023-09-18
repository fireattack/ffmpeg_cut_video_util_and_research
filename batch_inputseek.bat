ffmpeg -v error -ss 00:00:03 -i raw.ts -c copy input_seeking_copy.ts -y
ffmpeg -v error -ss 00:00:03 -i raw.ts -c copy input_seeking_copy_tomp4.mp4 -y
ffmpeg -v error -ss 00:00:03 -i raw.ts -c copy -avoid_negative_ts make_zero input_seeking_copy_tomp4_avoid_neg_ts.mp4 -y
ffmpeg -v error -ss 00:00:03 -i raw.ts -c copy input_seeking_copy_tomkv.mkv -y

ffmpeg -v error -ss 00:00:03 -i raw.ts -c:v libx264 -c:a aac input_seeking_encode.ts -y
ffmpeg -v error -ss 00:00:03 -i raw.ts -c:v libx264 -c:a aac input_seeking_encode_tomp4.mp4 -y
ffmpeg -v error -ss 00:00:03 -i raw.ts -c:v libx264 -c:a aac input_seeking_encode_tomkv.mkv -y