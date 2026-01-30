from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "courses"

urlpatterns = [
    path('', views.course_list, name="list"),
    path('course-new/', views.course_new, name="course-new"),
    path('<int:pk>/delete/', views.course_delete, name='course-delete'),
    path('course/<int:course_id>/', views.course_page, name="course-page"),
    path('enroll/<int:course_id>/', views.enroll_in_course, name='enroll'),
    path('<slug:slug>', views.course_list, name="course"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
