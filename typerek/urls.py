from django.urls import path
from . import views

urlpatterns = [
    path('', views.match, name='match'),
    path('match/<str:lg>/<int:pk>/',views.match_detail, name='match_detail'),
    path('quest/<str:lg>/<int:pk>/',views.question_detail, name='question_detail'),
    path('league/<str:lg>', views.league, name='league'),
    path('login', views.login_page, name='login_page'),
    path('logout', views.logout_page, name='logout_page'),
    path('rules', views.rules, name='rules'),



]