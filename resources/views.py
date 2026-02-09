from django.shortcuts import render, get_object_or_404, redirect
from .models import Resource
from .forms import ResourceForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/users/login/")
def resource_list(request, course_name=None):
    if course_name:
        resources = Resource.objects.filter(course=course_name)
    else:
        resources = Resource.objects.all()

    return render(request, "resources/resource_list.html", {
        "resources": resources,
        "course_name": course_name,
    })

@login_required(login_url="/users/login/")
def resource_page(request, slug):
    resource = get_object_or_404(Resource, slug=slug)
    return render(request, 'resources/resource_page.html', {'resource': resource})

@login_required(login_url="/users/login/")
def resource_new(request):
    if request.method == "POST":
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('resources:list')
    else:
        form = ResourceForm()
    return render(request, 'resources/resource_new.html', {'form': form})

def resource_delete(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == "POST":
        resource.delete()
        return redirect('resource:list')
    return redirect('resource:list')