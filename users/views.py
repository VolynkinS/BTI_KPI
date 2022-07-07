from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import UserLoginForm


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('kpi:home', pk=1)
    else:
        form = UserLoginForm()
    return render(request, 'users/user_login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('kpi:home', pk=1)
