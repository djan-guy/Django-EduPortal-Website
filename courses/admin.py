from django.contrib import admin
from .models import Course, Enrollment
from quizzes.models import Quiz

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrollment_date', 'is_active')
    list_filter = ('course', 'is_active')
    search_fields = ('user__username', 'course__name')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
