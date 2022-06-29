
from django.contrib import admin
from django.urls import path, include


from django.conf.urls.static import static
from video.views import server_static
from project.settings import DEBUG

urlpatterns = [
    path('', include('video.urls', namespace='video')),
    # path('static/<path:resource>', server_static, name='css')
    # path('admin/', admin.site.urls),
]
