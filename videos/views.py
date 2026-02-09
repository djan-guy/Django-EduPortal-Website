from django.shortcuts import render, get_object_or_404, redirect
from .models import Video
from .forms import VideoForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/users/login/")
def video_list(request, course_name=None):
    if course_name:
        videos = Video.objects.filter(course=course_name)
    else:
        videos = Video.objects.all()

    return render(request, "videos/video_list.html", {
        "videos": videos,
        "course_name": course_name,
    })

@login_required(login_url="/users/login/")
def video_page(request, slug):
    video = get_object_or_404(Video, slug=slug)
    return render(request, 'videos/video_page.html', {'video': video})

@login_required(login_url="/users/login/")
def video_new(request):
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('videos:list')
    else:
        form = VideoForm()
    return render(request, 'videos/video_new.html', {'form': form})

def video_delete(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.method == "POST":
        video.delete()
        return redirect('video:list')
    return redirect('video:list')