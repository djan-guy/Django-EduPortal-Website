from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment
from .forms import CourseForm

@login_required(login_url="/users/login/")
def course_list(request):
    courses = Course.objects.all()
    for course in courses:
        course.is_enrolled = course.enrollments.filter(user=request.user).exists()
    return render(request, 'courses/course_list.html', {"courses": courses})


@login_required(login_url="/users/login/")
def course_page(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/course_page.html', {'course': course})

@login_required(login_url="/users/login/")
def course_new(request):
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('courses:list')
    else:
        form = CourseForm()
    return render(request, 'courses/course_new.html', {'form': form})

@login_required(login_url="/users/login/")
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(
        user=request.user,
        course=course
    )
    return redirect('courses:course-page', course_id=course.id)

@login_required(login_url="/users/login/")
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        course.delete()
        return redirect('courses:list')
    return redirect('courses:list')
