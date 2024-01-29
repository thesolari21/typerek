from django.contrib import admin

# Register your models here.

from .models import Conf, League, Matches, Bets, UsersLeagues, Questions, Answers

class MatchesAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'league', 'date', 'multiplier','status')
    list_filter = ( 'league', 'date', 'multiplier','status')

class BetsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'status')
    list_filter = ('user', 'status')

class UserLeaguesAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'league')
    list_filter = ('user', 'league')

class LeaguesAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status')

class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'league', 'status')
    list_filter = ( 'league', 'status')

class AnswersAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'status')
    list_filter = ('user', 'status')

admin.site.register(Conf)
admin.site.register(League, LeaguesAdmin)
admin.site.register(Matches, MatchesAdmin)
admin.site.register(Bets, BetsAdmin)
admin.site.register(UsersLeagues, UserLeaguesAdmin)
admin.site.register(Questions, QuestionsAdmin)
admin.site.register(Answers, AnswersAdmin)
