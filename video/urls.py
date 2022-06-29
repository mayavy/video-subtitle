from django.urls import path
from django.shortcuts import redirect


from .views import VideoUpload, VideoSearch, About, video_aws_url

app_name = 'video'

urlpatterns = [

        path('', VideoUpload.as_view(), name='upload'),
        path('search/', VideoSearch.as_view(), name='search'),
        path('about/', About.as_view(), name='about'),
        path('download/<str:video_id>', video_aws_url, name='download'),

     
]