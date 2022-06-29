import re
import markdown

from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.core.exceptions import BadRequest
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage


from project.settings import BINARY_LOC, README_PATH,  temporary_storage
from project.aws_conf import AWS_MEDIA_DIR, AWS_STATIC_DIR, aws_downloader
from .tasks import Video, video_task
from query import Db_Handler


class VideoUpload(TemplateView):
    template_name = 'video/upload.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if kwargs.get('uploaded') != None:
            context['uploaded'] = kwargs.get('uploaded')

        return context

    def post(self, request, *args, **kwargs):

        for fileobject in request.FILES.getlist('files'):
            filename = temporary_storage.save(fileobject.name, fileobject)
            video_task.delay(filename, fileobject.name, BINARY_LOC)

        kwargs['uploaded'] = 'Video(s) uploaded'

        return self.get(request,  *args, **kwargs)


class VideoSearch(TemplateView):
    template_name = 'video/search.html'

    def post(self, request, *args, **kwargs):
        string = request.POST.get('sentence').lower()
        word_iter = Video.gen_word_iter(string)

        words = sorted(word_iter, key=lambda word: len(word), reverse=True)

        # list ( generator of list of entries  )
        word_data = list(Db_Handler().query_words(words))

        for entry_list in word_data:  # clean data for display
            if entry_list == []:
                entry_list += [{'video_name': "No record found",
                                'video_id': 'does_not_exist', 'ranges': ''}]
            else:
                for entry in entry_list:
                    try:
                        entry['video_name'] = entry['video_id'].split('_|_')[
                            1]  # remove uuid
                        del entry['word']
                    except Exception as e:
                        print('Hot-gates here', e)

        word_data = dict(zip(words, word_data))
        context = {'data': word_data}
        return render(request, 'video/videolist.html', context)


class About(TemplateView):
    template_name = 'video/about.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        with open(README_PATH, 'r') as file:
            about = file.read()
            about_html = markdown.markdown(about)
        context['about'] = about_html
        return context


def video_aws_url(request, video_id: str, *args, **kwargs):
    """
    Redirects to bucket/media files present on AWS-S3.
    """
    video_url = aws_downloader(AWS_MEDIA_DIR, video_id)
    if video_url is not None:
        return redirect(video_url, *args, permanent=False)
    else:
        raise BadRequest('error')


def server_static(request, resource: str, *args, **kwargs):
    """Redirects to bucket/static files present on AWS-S3."""
    static_url = aws_downloader(AWS_STATIC_DIR, resource)
    if static_url is not None:
        return redirect(static_url, *args, permanent=False)
    else:
        raise BadRequest('error')
