import django_tables2 as tables
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from .filters import ShowFilter
from .models import *


class GeneralEffectTotal(tables.Column):
    def render(self, value):
        return value.general_effect_total


class VisualTotal(tables.Column):
    def render(self, value):
        return value.visual_total


class MusicTotal(tables.Column):
    def render(self, value):
        return value.music_total


class ShowTable(tables.Table):
    competition = tables.Column()
    date = tables.Column(
        accessor="get_date",
        verbose_name="Date",
        order_by=("competition.competition_date"),
    )
    corp = tables.Column()
    general_effect = GeneralEffectTotal(order_by=("general_effect.general_effect_total"))
    visual = VisualTotal(order_by=("visual.visual_total"))
    music = MusicTotal(order_by=("music.music_total"))
    total_score = tables.Column()

    class Meta:
        model = Show
        fields = ["corp", "date", "competition", "general_effect", "visual", "music", "total_score"]


class CompetitionTable(tables.Table):
    corp = tables.Column()
    general_effect = GeneralEffectTotal(order_by=("general_effect.general_effect_total"))
    visual = VisualTotal(order_by=("visual.visual_total"))
    music = MusicTotal(order_by=("music.music_total"))
    total_score = tables.Column()

    class Meta:
        model = Show
        fields = ["corp", "general_effect", "visual", "music", "total_score"]


class FilteredShowView(SingleTableMixin, FilterView):
    table_class = ShowTable
    model = Show
    template_name = "pull/show_table.html"
    filterset_class = ShowFilter
