from django.conf.urls import url
from rango import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'category/(?P<category_name_slug>[\w\-]+)/$', # Store the sequence
        views.show_category, name='show_category')     # into <category_name_slug>
]
