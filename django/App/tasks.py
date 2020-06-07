from time import sleep
import random
import requests
import tempfile

from django.conf import settings

from App.celery import app
from App.models import Clip

from converter import Converter as VideoConverter

FILE_CHUNK_SIZE = 1024 * 1024
MP4_CONVERT_PARAMS = { 'format': 'mp4', 'audio': { 'codec': 'mp3' }, "video": {"codec": "h264", "width": 640, "height": 360 } }

@app.task(bind=True)
def download_original_file(self, clip_id):
    clip = Clip.objects.get(pk=clip_id)
    print(f'Downloading for {clip_id} from {clip.link}')
    with tempfile.NamedTemporaryFile() as temp_file:
        with requests.get(clip.link, stream=True) as response:
            print(f'Saving file for {clip_id} from {clip.link}')
            for chunk in response.iter_content(chunk_size=512):
                if chunk:
                    temp_file.write(chunk)
            downloaded_file = temp_file
            file_name = clip.hash_id + '.video_format_unknown'
            clip.original_file.save(file_name, downloaded_file)
            clip.original_name = file_name
            clip.save()

            make_thumbnail.delay(clip_id)
            print(f'Generation of a thumbnail for {clip_id} {clip.original_name} dispatched')
            convert_to_mp4.delay(clip_id)
            print(f'Convertation for {clip_id} {clip.original_name} dispatched')

@app.task(bind=True)
def make_thumbnail(self, clip_id):
    print(f'Generating thumbnail for id {clip_id}')
    clip = Clip.objects.get(pk=clip_id)
    clip_file = clip.original_file
    if clip_file:
        with tempfile.NamedTemporaryFile() as video_temp_file,\
             tempfile.NamedTemporaryFile() as thumbnail_temp_file:
            for chunk in clip_file.file.chunks(chunk_size=FILE_CHUNK_SIZE):
                video_temp_file.write(chunk)
            conv = VideoConverter()
            conv.thumbnail(video_temp_file.name, 1, thumbnail_temp_file.name)
            # TODO: check existence of converted file!
            # ...
            print(f'Thumbnail generated for {clip.original_name}')
            thumbname_file_name = f'{settings.S3_THUMBNAIL_PREFIX}/{clip.hash_id}.png'
            clip.thumbnail_file.save(thumbname_file_name, thumbnail_temp_file)

@app.task(bind=True)
def convert_to_mp4(self, clip_id):
    clip = Clip.objects.get(pk=clip_id)
    clip_file = clip.original_file
    print(f'Converting file {clip.original_name} for id {clip_id}')
    if clip_file:
        with tempfile.NamedTemporaryFile() as source_temp_file, \
             tempfile.TemporaryDirectory() as temp_dir:
            for chunk in clip_file.chunks(chunk_size=FILE_CHUNK_SIZE):
                source_temp_file.write(chunk)
            destination_file_name = f'{settings.S3_MP4_PREFIX}/{clip.hash_id}.mp4'
            converted_temp_file_name = f'{temp_dir}/{clip.hash_id}.mp4'
            conv = VideoConverter()
            convert = conv.convert(
                source_temp_file.name, converted_temp_file_name, MP4_CONVERT_PARAMS)
            for timecode in convert:
                print(f'\rConverting ({timecode:.2f}) ...')
            # TODO: check destination file created!
            # ...
            print(f'Converted {clip.original_name}')
            with open(converted_temp_file_name, 'rb') as converted_temp_file:
                clip.mp4_file.save(destination_file_name, converted_temp_file)
