from django.urls import path
from . import views

urlpatterns = [
    path('', views.match, name='match'),
    path('<str:lg>/<int:pk>/',views.match_detail, name='match_detail'),
    path('login', views.login_page, name='login_page'),
    path('logout', views.logout_page, name='logout_page'),
    path('<str:lg>', views.league, name='league'),

]