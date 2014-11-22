from django.http import HttpResponse
from django.shortcuts import render

from snipchatapp.models import Snippets, Users, Comments

def index(request):
    context = {'snippet': Snippets.objects.order_by('-pub_date')[:1][0]}
    return render(request, 'snippet/index.html', context)

def add_snippet(request):
    return render(request, 'snippet/add_snippet.html')
