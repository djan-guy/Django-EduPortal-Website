from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "video"

urlpatterns = [
    path("", views.video_list, name="list"),
    path('video-new/', views.video_new, name="video-new"),
    path('<int:pk>/delete/', views.video_delete, name='video-delete'),
    path("<str:course_name>/", views.video_list, name="list-by-course"),
    path('<slug:slug>', views.video_list, name="video"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)