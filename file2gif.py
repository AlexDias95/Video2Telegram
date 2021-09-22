import inotify.adapters
import os
import telegram
import ffmpy

TOKEN = os.getenv('BOT_TOKEN')
FOLDER = os.getenv('FOLDER', '/tmp/')
EXTENSION = os.getenv('EXTENSION', 'mp4')
EXTENSION2 = os.getenv('EXTENSION2', 'avi')
EXTENSION3 = os.getenv('EXTENSION2', 'mkv')
DESTINATION = os.getenv('DESTINATION')

bot = telegram.Bot(TOKEN)
notifier = inotify.adapters.InotifyTree(FOLDER)

for event in notifier.event_gen():  
    if event is not None:   
        if 'IN_CLOSE_WRITE' in event[1] and (EXTENSION in event[3] or EXTENSION2 in event[3] or EXTENSION3 in event[3]):
            file_path = event[2] + '/' + event[3]
            try:
                gif_path = '/tmp/file2mkv.mkv'
                subs_path = '/tmp/subs.srt'
                file_send_path = '/tmp/file2mkv.mp4'
                ff = ffmpy.FFmpeg(
                    inputs={file_path: None},
                    outputs={gif_path: '-vcodec libx265 -crf 28 -ss 00:05:00.0 -to 00:05:30.0 -map 0:v -map 0:a:m:language:jpn? -map 0:a:m:language:eng? -map 0:a:m:language:pt? -map 0:s:m:language:eng? -map 0:s? -c:s copy -disposition:a:0 default -disposition:s:0 default'}
                )
                ff.run()
                try:
                    ffs = ffmpy.FFmpeg(
                        inputs={gif_path: None},
                        outputs={subs_path: '-map 0:s:0'}
                    )
                    ffs.run()
                    fft = ffmpy.FFmpeg(
                        inputs={gif_path: None},
                        outputs={file_send_path: '-vf subtitles=' + subs_path}
                    )
                    fft.run()
                except:
                    fft = ffmpy.FFmpeg(
                        inputs={gif_path: None},
                        outputs={file_send_path: None}
                    )
                file_open = open(file_send_path, 'rb')
                bot.send_chat_action(DESTINATION, 'upload_video')
                bot.send_animation(DESTINATION, file_open, timeout=600)
            except:
                file_open = open(file_path, 'rb')
                bot.send_chat_action(DESTINATION, 'upload_document')
                bot.send_document(DESTINATION, file_open, timeout=600)
            os.remove(gif_path)
            os.remove(file_send_path)
