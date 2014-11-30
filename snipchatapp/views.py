from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
import json
from django.shortcuts import redirect
from snipchatapp.models import Snippets, Comments
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from random import randrange

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

def login(request):
    pass

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
        code = request.POST['code']
        user = User.objects.all()[0]
        identifier = random_identifier()
        snippet = Snippets(code=code, user=user, identifier=identifier,
                           pub_date=timezone.now())
        snippet.history = identifier + "|"
        snippet.save()
        response = {
            'success': 'true',
            'identifier': identifier
        }
        return HttpResponse(json.dumps(response),
                            content_type='application/json')
    else:
        return render(request, 'snippet/add_snippet.html')

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
