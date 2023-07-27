from django.urls import path

from .views import *

urlpatterns = [
    path('', view=home),
    path('pull/', view=welcome, name='pull-home'),
    path('pull/welcome/', view=welcome, name='pull-welcome'),
    path('pull/about/', view=about, name='pull-about')
]