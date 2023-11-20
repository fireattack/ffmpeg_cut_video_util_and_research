@REM input seeking
ffmpeg -v error -ss 00:00:01.5 -i raw.mp4 -c copy diffss_inputseek_1.5.mkv -y
ffmpeg -v error -ss 00:00:02 -i raw.mp4 -c copy diffss_inputseek_2.0.mkv -y
ffmpeg -v error -ss 00:00:02.5 -i raw.mp4 -c copy diffss_inputseek_2.5.mkv -y
ffmpeg -v error -ss 00:00:02.8 -i raw.mp4 -c copy diffss_inputseek_2.8.mkv -y
ffmpeg -v error -ss 00:00:03 -i raw.mp4 -c copy diffss_inputseek_3.0.mkv -y
ffmpeg -v error -ss 00:00:03.5 -i raw.mp4 -c copy diffss_inputseek_3.5.mkv -y

@REM input seeking, with mp4 output
ffmpeg -v error -ss 00:00:01.5 -i raw.mp4 -c copy diffss_inputseek_1.5.mp4 -y
ffmpeg -v error -ss 00:00:02 -i raw.mp4 -c copy diffss_inputseek_2.0.mp4 -y
ffmpeg -v error -ss 00:00:02.5 -i raw.mp4 -c copy diffss_inputseek_2.5.mp4 -y
ffmpeg -v error -ss 00:00:02.8 -i raw.mp4 -c copy diffss_inputseek_2.8.mp4 -y
ffmpeg -v error -ss 00:00:03 -i raw.mp4 -c copy diffss_inputseek_3.0.mp4 -y
ffmpeg -v error -ss 00:00:03.5 -i raw.mp4 -c copy diffss_inputseek_3.5.mp4 -y

@REM output seeking
ffmpeg -v error -i raw.mp4 -ss 00:00:01.5 -c copy diffss_outputseek_1.5.mkv -y
ffmpeg -v error -i raw.mp4 -ss 00:00:02 -c copy diffss_outputseek_2.0.mkv -y
ffmpeg -v error -i raw.mp4 -ss 00:00:02.5 -c copy diffss_outputseek_2.5.mkv -y
ffmpeg -v error -i raw.mp4 -ss 00:00:02.8  -c copy diffss_outputseek_2.8.mkv -y
ffmpeg -v error -i raw.mp4 -ss 00:00:03 -c copy diffss_outputseek_3.0.mkv -y
ffmpeg -v error -i raw.mp4 -ss 00:00:03.5 -c copy diffss_outputseek_3.5.mkv -y