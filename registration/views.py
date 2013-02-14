from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
# String and Random used for password generator
import string
import random

from .forms import UserCreateForm, ResetForm
from poker.models import PokerUser

def UserRegistration(request):

    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            # if player is staker, token is their own email. otherwise their token is their staker's email and
            # their relation is their staker
            if data.__getitem__('user_type') == '1':
                data.__setitem__('token', data.__getitem__('email'))
            else:
                staker = PokerUser.objects.get(email=data.__getitem__('token'))
                data.__setitem__('poker_relate', staker.id)
                data.__setitem__('token', '')
            new_user = form.save(data)
            return HttpResponseRedirect('/')
    else:
        form = UserCreateForm()
    initialData = {'form': form}
    csrfContext = RequestContext(request, initialData)
    return render_to_response('registration/register.html', csrfContext)


def LoginRequest(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render_to_response('registration/login.html', {'form': form}, context_instance=RequestContext(request))    
        else:
            return render_to_response('registration/login.html', {'form': form}, context_instance=RequestContext(request))    
    else:
        form = AuthenticationForm()
        context = {"form": form}
        return render_to_response('registration/login.html', context, context_instance=RequestContext(request))

def LogoutRequest(request):
    logout(request)
    return HttpResponseRedirect('/auth/login/')

def PasswordReset(request):
    if request.method == 'POST':
        form = ResetForm(request.POST)
        if form.is_valid():
            userEmail = form.cleaned_data['email']
            user = PokerUser.objects.get(email=userEmail)
            if user is not None:
                newPass = PasswordGenerator()
                user.set_password(newPass)
                user.save()
                site = 'notecard.herokuapp.com'
                from_add = 'admin@notecard.herokuapp.com'
                to = user.email
                subject = 'Notecards! requested password update'
                body = 'Please visit %s and login with your new password below.\n Your new password is: %s \n\n Please do not reply to this email. If you have any questions please email DHoerst1@gmail.com' % (site, newPass)
                send_mail(subject, body, from_add, [user.email], fail_silently=False)
                return render_to_response('registration/reset.html', context_instance=RequestContext(request))
            else:
                reset_error = 'No account with that email address currently exists'
                return render_to_response('registration/passwordreset.html', {'form': form, 'reset_error': reset_error}, context_instance=RequestContext(request))
        else:
            return render_to_response('registration/passwordreset.html', {'form': form,}, context_instance=RequestContext(request))
    else:
        form = ResetForm()
        context = {"form": form}
        return render_to_response('registration/passwordreset.html', context, context_instance=RequestContext(request))

def PasswordGenerator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
