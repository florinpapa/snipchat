from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
import json
from django.shortcuts import redirect
from snipchatapp.models import Snippets, Users, Comments
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


def index(request):
    context = {'snippet': Snippets.objects.order_by('-pub_date')[:1][0]}
    return render(request, 'snippet/index.html', context)

def view_snippet(request, snippet_id):
    snippet = Snippets.objects.get(identifier=snippet_id)
    version_date = []
    versions = snippet.history.split('|')[:-1]
    for i in range(len(versions)):
        current_version = []
        current_version.append(i)
        full_date = Snippets.objects.get(identifier=versions[i]).pub_date
        date_str = full_date.strftime("%d/%m/%Y")
        time_str = full_date.strftime("%H:%M")
        current_version.append(date_str + " " + time_str)
        version_date.append(current_version)
    context = {
            'snippet': snippet,
            'version_date': version_date 
            }
    return render(request, 'snippet/index.html', context)

def add_snippet(request):
    if request.method == 'POST':
        code = request.POST['code']
        user = Users.objects.all()[0]
        identifier = random_identifier()
        snippet = Snippets(code=code, user=user, identifier=identifier,
                           pub_date=timezone.now())
        snippet.history = identifier + "|"
        snippet.save()
        return redirect('/snippet/snippet/' + identifier)
    else:
        return render(request, 'snippet/add_snippet.html')

def new_version(request, snippet_id):
    if request.method == 'POST':
        old_snippet = Snippets.objects.get(identifier=snippet_id)
        code = request.POST['code']
        user = Users.objects.all()[0]
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
