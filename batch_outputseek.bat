ffmpeg -v error -i raw.ts -ss 00:00:03 -c copy output_seeking_copy.ts -y
ffmpeg -v error -i raw.ts -ss 00:00:03 -c copy output_seeking_copy_tomp4.mp4 -y
ffmpeg -v error -i raw.ts -ss 00:00:03 -c copy output_seeking_copy_tomkv.mkv -y

ffmpeg -v error -i raw.ts -ss 00:00:03 -c:v libx264 -c:a aac output_seeking_encode.ts -y
ffmpeg -v error -i raw.ts -ss 00:00:03 -c:v libx264 -c:a aac output_seeking_encode_tomp4.mp4 -y
ffmpeg -v error -i raw.ts -ss 00:00:03 -c:v libx264 -c:a aac -vsync 0 output_seeking_encode_tomp4_vsync0.mp4 -y
ffmpeg -v error -i raw.ts -ss 00:00:03 -c:v libx264 -c:a aac output_seeking_encode_tomkv.mkv -y