from django.contrib import messages
from turtle import right
from django.shortcuts import redirect, render
from projects.forms import ProjectForm, ReviewForm
from .models import Project, Tag
from django.contrib.auth.decorators import login_required
from .utils import searchProject, paginate_projects



def projects(request, pk):
    try:
        project_obj = Project.objects.get(title=pk)
    except:
        project_obj = {'title': 'Not found'}

    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.owner = request.user.profile
        review.project = project_obj
        review.save()
        project_obj.update_info
        messages.success(request, 'your review submitted !')
        return redirect('find', pk=project_obj)

    return render(request, 'projects/single_project.html', {'project': project_obj, 'form': form})


@login_required(login_url='login')
def add_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user.profile
            project.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


def all_projects(request):
    search_query, projects = searchProject(request)
    
    custom_range, projects = paginate_projects(request, projects, 6)

    return render(request, 'projects/index.html', {'projects': projects, 'search_query': search_query,
                    'custom_range': custom_range})


def update_project(request, pk):
    project = Project.objects.get(title=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        new_tags = request.POST.get('newTags').replace(',', ' ').split()
        if form.is_valid():
            for tag in new_tags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            form.save()
            return redirect('account')
    form = ProjectForm(instance=project)
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


def delete_project(request, pk):
    project = Project.objects.get(title=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('account')
    else:
        return render(request, 'delete_template.html', {'object': project})
