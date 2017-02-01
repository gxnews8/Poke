from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^main$', views.index, name = 'main'),
    url(r'^register$', views.register, name = 'register'),
    url(r'^login$', views.login, name = 'login'),
    url(r'^pokes$', views.pokes, name = 'pokes'),
    url(r'^logout$', views.logout, name = 'logout'),
]
