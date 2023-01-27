from django.urls import path
from .src import configs as c
from . import views

urlpatterns = [
    path(conf['url'], getattr(views, conf['view_name']).as_view())
    for conf in c.LIST
]
