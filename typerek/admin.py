from django.contrib import admin

# Register your models here.

from .models import Conf, League, Matches, Bets, UsersLeagues, Questions, Answers, CategoryArticles, Articles, Rules, UserProfile

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

class CategoryArticlesAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'category')


class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'title' ,'category', 'status')
    list_filter = ('category', 'status')

class RulesAdmin(admin.ModelAdmin):
    list_display = ('__str__' , 'game_rules' )

admin.site.register(Conf)
admin.site.register(League, LeaguesAdmin)
admin.site.register(Matches, MatchesAdmin)
admin.site.register(Bets, BetsAdmin)
admin.site.register(UsersLeagues, UserLeaguesAdmin)
admin.site.register(Questions, QuestionsAdmin)
admin.site.register(Answers, AnswersAdmin)
admin.site.register(CategoryArticles, CategoryArticlesAdmin)
admin.site.register(Articles, ArticlesAdmin)
admin.site.register(Rules, RulesAdmin)
admin.site.register(UserProfile)
