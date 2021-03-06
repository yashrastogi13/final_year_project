from django.shortcuts import render,redirect
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)

from .forms import UserLoginForm,UserRegisterForm
# Create your views here.

def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/posts/')

    context = {
        'form':form
    }
    return render(request, 'main/login.html', context)

def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(request,username=user.username, password=user.password)
        #login(request, new_user)
        if next:
            return redirect('login_view')
        return redirect('/')

    context = {
        'form':form,
    }
    return render(request, 'main/signup.html', context)

def logout_view(request):
    logout(request)
    # return reverse_lazy(request, 'main/home.html')
    # return render(request, 'main/home.html')
    return redirect('/')