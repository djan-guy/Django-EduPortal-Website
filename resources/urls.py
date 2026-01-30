from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "resource"

urlpatterns = [
    path("", views.resource_list, name="list"),
    path('resource-new/', views.resource_new, name="resource-new"),
    path('<int:pk>/delete/', views.resource_delete, name='resource-delete'),
    path("<str:course_name>/", views.resource_list, name="list-by-course"),
    path('<slug:slug>', views.resource_list, name="resource"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)