from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from App.tasks import (
    make_thumbnail,
    convert_to_mp4,
    download_original_file
)
from App.forms import NewClipForm
from App.models import Clip

@require_http_methods(["GET"])
def index(request):
    clips = Clip.objects.all()
    return render(
        request,
        'index.html', 
        context={'form': NewClipForm, 'clips': clips})

@require_http_methods(["POST"])
def new(request):
    if request.method == "POST":
        form = NewClipForm(request.POST, request.FILES)
        if form.is_valid():
            form_data = form.cleaned_data
            link = form_data.get('clip_link', False)
            clip_file = request.FILES.get('clip_file', None)
            # Case: file uploaded
            if clip_file:
                new_clip = Clip(
                    original_name=clip_file.name,
                    original_file=clip_file)
                clip = new_clip.save()
                print(f'Clip saved with id {clip.pk}')
                make_thumbnail.delay(clip.pk)
                print(f'Generation of a thumbnail for {clip.pk} {clip_file.name} dispatched')
                convert_to_mp4.delay(clip.pk)
                print(f'Convertation for {clip.pk} {clip_file.name} dispatched')
                messages.success(request, f'File {clip_file.name} added')
            # Case: link provided
            elif link:
                new_clip = Clip(link=link)
                clip = new_clip.save()
                print(f'Clip saved with id {clip.pk}')
                download_original_file.delay(clip.pk)
                messages.success(request, f'Link {link} added to download quiue')

    return HttpResponseRedirect('/')
