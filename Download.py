import yt_dlp
from mutagen.mp4 import MP4
import tempfile
import pydub
import os


def download_audio(link):
  with yt_dlp.YoutubeDL({'extract_audio': True, 'format': 'm4a','addmetadata':True, 'outtmpl': '%(title)s.m4a'}) as video:
    info_dict = video.extract_info(link, download = True)
    video_title = info_dict['title']
    channel_title = info_dict['uploader']
    video.download(link)
    audio = pydub.AudioSegment.from_file(f'{video_title}.m4a', format='m4a')
    os.unlink(f'{video_title}.m4a')
    audio.export(f'{video_title}.mp3', format='mp3')
    return [f'{video_title}.mp3', video_title, channel_title]
