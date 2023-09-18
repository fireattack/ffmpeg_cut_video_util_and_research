mkdir test2
copy /Y raw-longer.ts test2\raw.ts

ffmpeg -v error -ss 3 -i test2\raw.ts -c copy test2\intermediate.ts -y
ffmpeg -v error -ss 3 -i test2\raw.ts -c copy test2\intermediate.mp4 -y

ffmpeg -v error -ss 6 -i test2\intermediate.ts -c copy test2\raw_to_interts_tots.ts -y
ffmpeg -v error -ss 6 -i test2\intermediate.ts -c copy test2\raw_to_interts_tomp4.mp4 -y
ffmpeg -v error -ss 6 -i test2\intermediate.mp4 -c copy test2\raw_to_intermp4_tomp4.mp4 -y
ffmpeg -v error -ss 6 -i test2\intermediate.mp4 -c copy test2\raw_to_intermp4_tots.ts -y

ffmpeg -v error -i test2\raw.ts -c copy test2\raw.mp4 -y
ffmpeg -v error -ss 9 -i test2\raw.mp4 -c copy test2\rawfixmp4_directly_tomp4.mp4 -y
ffmpeg -v error -ss 9 -i test2\raw.mp4 -c copy test2\rawfixmp4_directly_tots.ts -y