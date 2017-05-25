from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^post_url/$', views.post_service, name='post_service'),
    url(r'^import_csv/$', views.get_import, name='get_import')
]
