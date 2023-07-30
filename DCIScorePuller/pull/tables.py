import django_tables2 as tables
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from .filters import ShowFilter
from .models import Show


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
    corp = tables.Column()
    general_effect = GeneralEffectTotal()
    visual = VisualTotal()
    music = MusicTotal()
    total_score = tables.Column()

    class Meta:
        model = Show

class FilteredShowView(SingleTableMixin, FilterView):
    table_class = ShowTable
    model = Show
    template_name = "pull/show_table.html"
    filterset_class = ShowFilter