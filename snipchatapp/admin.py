from django.contrib import admin
from snipchatapp.models import Snippets, Comments, Users

admin.site.register(Snippets)
admin.site.register(Comments)
admin.site.register(Users)
