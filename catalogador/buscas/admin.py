from django.contrib import admin
from buscas.models import Paridade, Configuraçõe, Chance, Vela


class VelasAdmin(admin.ModelAdmin):
    fields = (('par', 'timeframe'), 'data', 'direc')
    list_display = ('data', 'par', 'Horário', 'Direção')
    search_fields = ['par', 'timeframe', 'hora', 'minuto']
    list_filter = ('par', 'data', 'timeframe')

    search_help_text = 'Par Timeframe Hora Minuto'
    sortable_by = ['direc']

    @admin.display(ordering='data')
    def dia(self, obj):
        return obj.data.first_name

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request, queryset, search_term,
        )
        try:
            search_term_as_int = int(search_term)
        except ValueError:
            pass
        else:
            queryset |= self.model.objects.filter(age=search_term_as_int)
        return queryset, may_have_duplicates



admin.site.register(Paridade)
admin.site.register(Configuraçõe)
admin.site.register(Chance)
admin.site.register(Vela, VelasAdmin)