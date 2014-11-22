from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

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
    context = {'snippet': Snippets.objects.get(identifier=snippet_id)}
    return render(request, 'snippet/index.html', context)

def add_snippet(request):
    if request.method == 'POST':
        code = request.POST['code']
        user = Users.objects.all()[0]
        identifier = random_identifier()
        snippet = Snippets(code=code, user=user, identifier=identifier, pub_date=timezone.now())
        snippet.save()
        return view_snippet(request, identifier)
        #return render(request, 'snippet/add_snippet.html')
    else:
        return render(request, 'snippet/add_snippet.html')



