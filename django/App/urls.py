from django.conf.urls import url
from App import views

app_name = 'App'

urlpatterns = [
    url(r'new/', views.new, name='new'),
    url(r'', views.index, name='index'),
]
