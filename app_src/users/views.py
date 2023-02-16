# Python-native libraries
import time
from datetime import datetime
from typing import Optional

# 3rd party libraries
from django.db import transaction
from django.views import View
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.conf import settings

# Project-defined imports
from .forms import LoginForm
from utils.timing_defenses import calc_remaining_time_for_report_error

User = get_user_model()


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('planted_trees')
        return render(request, 'auth/login.html', {'login_form': LoginForm()})

    # I personally don't like much working with Django-forms (they tend to slows down page renders very easily when 
    # poorly planned), I rather prefer working directly with an API authentication method returning JWT tokens.
    # This authentication was made using Django Forms only to demonstrate I know how to work with it.
    @transaction.atomic # Avoids creating user if there is an error during the process
    def post(self, request):
        started_at = datetime.now()
        form = LoginForm(request.POST)

        if not form.is_valid():
            time.sleep(calc_remaining_time_for_report_error(started_at))
            return render(request, 'auth/login.html', {'login_form': form})

        username: str = form.cleaned_data['username']
        password: str = form.cleaned_data['password']

        user: Optional[User] = auth.authenticate(request, username=username, password=password)

        if user is None:
            time.sleep(calc_remaining_time_for_report_error(started_at))
            # Do not show "user does not exist" to avoid user enumeration attacks
            form.add_error(None, 'Invalid username or password')
            return render(request, 'auth/login.html', {'login_form': form})
        
        auth.login(request, user)
        request.session.set_expiry(settings.SESSION_EXPIRE_SECONDS)
        print(f"User {user.username} logged in. Redirecting to {settings.LOGIN_REDIRECT_URL}")
        return redirect(settings.LOGIN_REDIRECT_URL)


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            auth.logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)
