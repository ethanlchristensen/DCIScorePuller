from django.urls import path

from .views import *

urlpatterns = [
    path("", view=home),
    path("pull/", view=home, name="pull-home"),
    path("pull/welcome", view=welcome, name="pull-welcome"),
    path("pull/about", view=about, name="pull-about"),
    path("pull/admin", view=admin, name="pull-admin"),
    path("pull/scrape", view=scrape, name="pull-scrape"),
    path("pull/show/table", view=show_table, name="show-table"),
    path("pull/autocomplete", view=autocomplete_search, name="autocomplete"),
    path("pull/chart/rank/<str:rank_type>", view=rank_chart, name="rank-chart"),
    path("pull/chart/competition/<str:competition>", view=competition_chart, name="competition-chart")
]
