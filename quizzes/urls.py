from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "quizzes"

urlpatterns = [
    path('', views.quiz_list_all, name="list"),
    path('course/<int:course_id>/', views.quiz_list_by_course, name="by-course"),
    path('quiz-new/', views.quiz_new, name="quiz-new"),
    path('quiz/<int:quiz_id>/', views.quiz_page, name="quiz-page"),
    path('<int:pk>/delete/', views.quiz_delete, name='quiz-delete'),
    path('quiz/<int:quiz_id>/submit/', views.quiz_submit, name="quiz-submit"),
    path('quiz/<int:quiz_id>/results/', views.quiz_results, name="quiz-results"),
    path('<int:quiz_id>/teacher-results/', views.quiz_results_teacher, name='quiz-results-teacher'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
