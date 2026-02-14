from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserUpdateForm
from .forms import UserRegisterForm



# Create your views here.

def home(request):
    return render(request, 'blog/base.html')

def posts(request):
    return render(request, 'blog/base.html')

def register(request):
    return render(request, 'blog/base.html')

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'blog/profile.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'blog/register.html', {'form': form})

