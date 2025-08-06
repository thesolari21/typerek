from django.urls import path
from . import views

app_name = 'typerek'

urlpatterns = [
    path('', views.match, name='match'),
    path('match/<str:lg>/<int:pk>/',views.match_detail, name='match_detail'),
    path('quest/<str:lg>/<int:pk>/',views.question_detail, name='question_detail'),
    path('league/<str:lg>', views.league, name='league'),
    path('login', views.login_page, name='login_page'),
    path('logout', views.logout_page, name='logout_page'),
    path('rules', views.rules, name='rules'),
    path('articles', views.articles, name='articles'),
    path('articles/<int:article_id>/', views.article_detail, name='article_detail'),
    path('articles/<int:article_id>/edit/', views.edit_article, name='edit_article'),
    path('articles/add/', views.add_article, name='add_article'),
    path('list_of_all_matches', views.list_of_all_matches, name='list_of_all_matches'),
    path('list_of_all_matches/<int:match_id>/edit/', views.edit_match, name='edit_match'),
    path('list_of_all_matches/add/', views.add_match, name='add_match'),
    path('list_of_all_questions', views.list_of_all_questions, name='list_of_all_questions'),
    path('list_of_all_questions/<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('list_of_all_questions/add/', views.add_question, name='add_question'),
    path('rules/edit/', views.edit_rules, name='edit_rules'),
    path('edit_user_profile', views.edit_user_profile, name='edit_user_profile'),
    path('user/<str:username>/', views.display_user, name='display_user'),


]