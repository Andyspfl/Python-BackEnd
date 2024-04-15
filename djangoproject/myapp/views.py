# from django.shortcuts import render
from django.http import HttpResponse
from .models import Project, Task
from django.shortcuts import get_object_or_404, render, redirect
from .forms import CreateNewTask, CreateNewProject



# Create your views here.
def index(request):
    title = "Django Course"
    return render(request, 'index.html', {
        'title': title
    })
def hello(request, username):
    return HttpResponse("<h1>Hello word %s</h1>" % username)
def about(request):
    return render(request, 'about.html')

def projects(request):
    # projects = list(Project.objects.values())
    projects = Project.objects.all()
    return render(request, 'project/project.html', {"projects" :projects})

def tasks(request):
    # task =get_object_or_404(Task, id=id)
    tasks = Task.objects.all()
    return render(request, 'tasks/task.html',{"tasks":tasks})

def create_task(request):
    if request.method =='GET':
        return render(request, "tasks/create_task.html", {"form": CreateNewTask})
    else:
        Task.objects.create(title=request.POST["title"], decription=request.POST["description"], project_id=2)
        return redirect("task")
    
def create_project(request):
    if request.method =='GET':
        return render(request, 'project/create_project.html',{"form":CreateNewProject})
    else:
        Project.objects.create(name=request.POST["name"])
        return redirect("project")
    