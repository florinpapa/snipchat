from django.contrib import admin
from snipchatapp.models import Snippets, Comments
from django.contrib.auth.models import User

admin.site.register(Snippets)
admin.site.register(Comments)
