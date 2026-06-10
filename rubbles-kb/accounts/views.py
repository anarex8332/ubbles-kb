from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, UserEmailForm
from .models import UserProfile


def register_view(request):
    if request.user.is_authenticated:
        return redirect('knowledge:home')
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('knowledge:home')
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('knowledge:home')
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        next_url = request.GET.get('next', 'knowledge:home')
        return redirect(next_url)
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def profile_view(request):
    """Страница профиля пользователя"""
    return render(request, 'accounts/profile.html', {
        'profile_user': request.user,
    })


@login_required
def profile_edit(request):
    """Редактирование профиля"""
    # Создаём профиль, если его нет (для старых пользователей)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    email_form = UserEmailForm(instance=request.user)
    profile_form = UserProfileForm(instance=profile)

    if request.method == 'POST':
        email_form = UserEmailForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if email_form.is_valid() and profile_form.is_valid():
            email_form.save()
            profile_form.save()
            return redirect('profile')

    return render(request, 'accounts/profile_edit.html', {
        'email_form': email_form,
        'profile_form': profile_form,
    })
