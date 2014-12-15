from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
  url(r'^snippet/', include('snipchatapp.urls')),
  url(r'^admin/', include(admin.site.urls)),
  url(r'^$', 'snipchatapp.views.add_snippet'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
