from email import message
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from .models import Profile, Skill
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomProfileCreationForm, SkillForm, MessageForm
from django.contrib.auth.decorators import login_required
from .utils import searchProfiles, paginate_profiles

def profile(request, name):
    profile = Profile.objects.get(name=name)
    if profile == request.user.profile:
        return redirect('account')
    topSkills = profile.skill_set.exclude(description = "")
    otherSkills = profile.skill_set.filter(description = "")
    context = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, 'users/profile.html', context)

def index(request):
    search_query, profiles = searchProfiles(request)
    custom_range, profiles = paginate_profiles(request, profiles, 6)
    context = {'profiles': profiles, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'users/index.html', context)


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('projects')
        
    if request.method == 'POST':
        try:
            user = authenticate(
                request,
                username=request.POST['username'],password=request.POST['password']
                )
            if user is not None:
                login(request, user)
                return redirect(request.GET['next'] if 'next' in request.GET else 'account')

        except:
            messages.error(request, 'wrong password or username !')

    context = {'page': 'login'}
    return render(request, 'users/login_register.html', context)


def registerUser(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'user registered successfully !')
            login(request, user)
            return redirect('account')
        else:
            messages.error(request, 'something wnet wrong !')
    form = CustomUserCreationForm()
    context = {'page': 'register', 'form': form}
    return render(request, 'users/login_register.html', context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    messages.info(request, 'user logged out !')
    return redirect('login')


@login_required(login_url='login')
def account(request):
        profile = request.user.profile
        skills = profile.skill_set.all()
        context = {'profile': profile, 'skills': skills}
        return render(request, 'users/account.html', context)


@login_required(login_url='login')
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = CustomProfileCreationForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    form = CustomProfileCreationForm(instance=profile)
    context = {'form': form}
    return render(request, 'users/edit-profile.html', context)

@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        return redirect('account')
    context = {'object': skill}
    return render(request, 'delete_template.html', context)


@login_required(login_url='login')
def editSkill(request, pk):
    skill = Skill.objects.get(id=pk)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            skill.save()
            return redirect('account')
    form = SkillForm(instance=skill)
    context = {'form': form}
    return render(request, 'users/edit-skill.html', context)


@login_required(login_url='login')
def addSkill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = request.user.profile
            skill.save()
            return redirect('account')
    form = SkillForm()
    context = {'form': form}
    return render(request, 'users/edit-skill.html', context)


@login_required(login_url='login')
def inbox(request):
    messages = request.user.profile.messages.all()
    unreadCount = messages.filter(is_read=False).count()
    context = {'message': messages, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def view_message(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if not message.is_read:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)


def send_message(request, pk):
    form = MessageForm()
    profile = Profile.objects.get(name=pk)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        message = form.save(commit=False)
        message.recipient = profile
        if request.user.is_authenticated:
            message.sender = request.user.profile
            message.name = request.user.profile.name
            message.email = request.user.profile.email
        message.save()
        messages.success(request, 'message successfully sent')
        return redirect('profile', pk)
    context = {'form': form, 'profile': profile}
    return render(request, 'users/message-form.html', context)