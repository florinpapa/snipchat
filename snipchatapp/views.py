from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
import json
from django.shortcuts import redirect
from snipchatapp.models import Snippets, Comments
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout as django_logout
from django.contrib.auth import authenticate, login as django_login
from random import randrange
from django import forms

def generate():
  if randrange(10) > 5:
    return chr(randrange(97, 123))
  else:
    return randrange(10)

def random_identifier():
    xs = []
    for i in range(0,6):
        xs.append(generate())
    return "".join(str(x) for x in xs)

def inline_comment_html(request):
    if request.method == 'POST':
        context = {
                'snippet_id': request.POST['snippet_id']
                }
        return render(request, 'inline_comment_markup.html', context)
    else:
        response = {
            'success': 'false',
            'message': 'Must make a POST call'
        }
        return HttpResponse(json.dumps(response),
                            content_type='application/json')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return redirect('add_snippet')
    else:
        form = UserCreationForm()
    return render(request, "register.html", {
        'form': form,
    })

class LoginForm(forms.Form):
    username = forms.CharField(label='Username',
                               max_length=100, required=True)
    password = forms.CharField(label='Password',
                               max_length=100, required=True,
                               widget=forms.PasswordInput())
    class Meta:
        model = User

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username,
                                     password=password)
            if user is not None and user.is_active:
                django_login(request, user)
                return redirect('profile', user.username)
    else:
        form = LoginForm()
    return render(request, 'login.html', {
        'form': form    
    })

def log_out(request):
    logout(request)
    return redirect('logout')

def logout(request):
    print request.user.is_authenticated()
    return render(request, 'logout.html')

def add_comment(request, snippet_id):
    if request.method == 'POST' and \
            request.user.is_authenticated():
        snippet = Snippets.objects.get(identifier=snippet_id)
        comment = Comments(comment=request.POST['comment'],
                           user=request.user,
                           row=request.POST['row'],
                           snippet=snippet,
                           pub_date=timezone.now())
        comment.save()
        response = {
            'success': 'true'
        }
        return HttpResponse(json.dumps(response),
                            content_type='application/json')
    else:
        response = {
            'success': 'false',
            'message': 'Must be authenticated'
        }
        return HttpResponse(json.dumps(response),
                            content_type='application/json')

def index(request):
    context = {'snippet': Snippets.objects.order_by('-pub_date')[:1][0]}
    return render(request, 'snippet/index.html', context)

def view_snippet(request, snippet_id):
    snippet = Snippets.objects.get(identifier=snippet_id)
    version_date = []
    versions = snippet.history.split('|')[:-1]
    comments = Comments.objects.all().filter(snippet=snippet)
    for i in range(len(versions)):
        current_version = []
        current_version.append(versions[i])
        full_date = Snippets.objects.get(identifier=versions[i]).pub_date
        date_str = full_date.strftime("%d/%m/%Y")
        time_str = full_date.strftime("%H:%M")
        current_version.append(date_str + " " + time_str)
        version_date.append(current_version)
    context = {
            'snippet': snippet,
            'version_date': version_date,
            'comments': comments 
            }
    return render(request, 'snippet/index.html', context)

def add_snippet(request):
    if request.method == 'POST':
        if request.user and request.user.is_authenticated():
            code = request.POST['code']
            user = request.user
            identifier = random_identifier()
            snippet = Snippets(code=code, user=user, identifier=identifier,
                               pub_date=timezone.now())
            snippet.history = identifier + "|"
            snippet.save()
            response = {
                'success': 'true',
                'identifier': identifier
            }
        else:
            response = {
                'success': 'false',
                'message': 'You are not authenticated'
            }
        return HttpResponse(json.dumps(response),
                            content_type='application/json')
    else:
        print request.user
        return render(request, 'snippet/add_snippet.html', request)

def new_version(request, snippet_id):
    if request.method == 'POST':
        old_snippet = Snippets.objects.get(identifier=snippet_id)
        code = request.POST['code']
        user = User.objects.all()[0]
        identifier = random_identifier()
        snippet = Snippets(code=code, user=user, identifier=identifier,
                           revision=old_snippet.revision + 1,
                           pub_date=timezone.now())
        snippet.history = old_snippet.history + identifier + "|"
        snippet.save()
        response = {
            'success': 'true',
            'identifier': identifier
        }
        return HttpResponse(json.dumps(response),
                            content_type='application/json')
    else:
        response = {
            'success': 'false',
            'message': 'Must make a POST call'
        }
        return HttpResponse(json.dumps(response),
                            content_type='application/json')

def profile(request, username):
    if request.user.is_authenticated():
        current_user = User.objects.get(username=username)
        user_snippets = Snippets.objects.all().filter(user=current_user)
        context = {
            'user': username,
            'snippets': user_snippets
        }
        return render(request, 'profile.html', context)
    else:
        return redirect('login')
