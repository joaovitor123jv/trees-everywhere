# Python-native libraries
import time
from datetime import datetime

# 3rd party libraries
from django.views import View
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.conf import settings

# Project-defined imports
from .forms import LoginForm

User = get_user_model()


# Used to prevent time-based attacks on user authentication (more on calc_remaining_time_for_report_error function)
MINIMUM_TIME_FOR_REPORT_ERROR = 1000 # In miliseconds

# Password and e-mail with at least 6 characters
MINIMUM_CREDENTIAL_SIZE = 6

def calc_remaining_time_for_report_error(request_started_at: datetime) -> int:
    """
        Calculates a time before returning response to client. This is used with MINIMUM_TIME_FOR_REPORT_ERROR to 
        prevent time-based attacks.

        To learn more about time-based attacks, refer to:
        https://ropesec.com/articles/timing-attacks/#:~:text=A%20timing%20attack%20is%20a,the%20password%20of%20a%20user
    """
    now = datetime.now()
    elapsed_time = now - request_started_at

    # If the maximum time was already reached for any reason, do not delay
    if elapsed_time > MINIMUM_TIME_FOR_REPORT_ERROR:
        return 0

    time_to_sleep = MINIMUM_TIME_FOR_REPORT_ERROR - elapsed_time
    return time_to_sleep


def is_invalid_credential(received_credential: str) -> bool:
    """
        Given a credential, checks for characters thant can't be entered through the designed template, detecting possible threats

        If credential is invalid, returns True, otherwise it returns False
    """
    INVALID_CHARS = [' ', '\n', '\r']
    has_invalid_chars = any([char in INVALID_CHARS for char in received_credential])
    has_invalid_size = len(received_credential) < MINIMUM_CREDENTIAL_SIZE

    return has_invalid_chars or has_invalid_size


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(settings.LOGGED_IN_FIRST_PAGE)
        return render(request, 'auth/login.html', {'login_form': LoginForm()})

    # I personally don't like much working with Django-forms (they tend to slows down page renders very easily when 
    # poorly planned), I rather prefer working directly with an API authentication method returning JWT tokens.
    # This authentication was made using Django Forms only to demonstrate I know how to work with it.
    def post(self, request):
        started_at = datetime.now()
        form = LoginForm(request.POST)

        if not form.is_valid():
            time.sleep(calc_remaining_time_for_report_error(started_at))
            return render(request, 'auth/login.html', {'login_form': form})

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = auth.authenticate(request, username=username, password=password)

        if user is None:
            time.sleep(calc_remaining_time_for_report_error(started_at))
            return render(request, 'auth/login.html', {'login_form': form})
        
        auth.login(request, user)
        request.session.set_expiry(settings.SESSION_EXPIRE_SECONDS)
        print(f"User {user.username} logged in. Redirecting to {settings.LOGGED_IN_FIRST_PAGE}")
        return redirect(settings.LOGGED_IN_FIRST_PAGE)


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            auth.logout(request)
        return redirect(settings.GUEST_FIRST_PAGE)
