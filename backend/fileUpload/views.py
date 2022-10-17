from django.shortcuts import render
from .models import FileObject
from social_django.models import UserSocialAuth
# from social_django 
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    object_list = None
    if request.user.is_authenticated:
        object_list = FileObject.objects.filter(owner__username=request.user.username)
        if request.user.username == 'admin':
            object_list = FileObject.objects.all()
    return render(request, 's3objects/home.html', {'object_list': object_list})


def account(request):
    user_list = UserSocialAuth.objects.all()
    return render(request, 's3objects/account.html', {'sau': user_list})


from django import forms
from django.http import HttpResponseRedirect


class S3ObjectForm(forms.ModelForm):
    class Meta:
        model = FileObject
        fields = ['file', 'description']
        exclude = ('owner',)


def uploadFile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = S3ObjectForm(request.POST, request.FILES)
            if form.is_valid():
                new_s3object = form.save(commit=False)
                new_s3object.owner = request.user
                new_s3object = form.save()
                return HttpResponseRedirect('/')
        else:
            form = S3ObjectForm()
        return render(request, 's3objects/upload.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')


def updateFile(request, id):
    if request.user.is_authenticated and FileObject.objects.get(pk=id).owner == request.user:
        old_file = FileObject.objects.get(pk=id)
        form = S3ObjectForm(request.POST or None, request.FILES, instance=old_file)
        if request.POST and form.is_valid():
            form.save()
            return HttpResponseRedirect('/')

        return render(request, 's3objects/upload.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')


def deleteFile(request, id):
    if request.user.is_authenticated and (FileObject.objects.get(pk=id).owner == request.user or request.user == "admin") :
        sel_file = FileObject.objects.get(pk=id)
        if request.method == 'POST':
            sel_file.delete()
            return HttpResponseRedirect('/')

        return render(request, 's3objects/delete.html', {'sel_file': sel_file})
    else:
        return HttpResponseRedirect('/login/')


from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                new_user = form.save()
                return HttpResponseRedirect('/')
        else:
            form = RegistrationForm()
        return render(request, 's3objects/registration/register.html', {'form': form})
