from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('articles/<int:id>/', views.article, name='articles'),
    path('categories/<str:category>/', views.category, name='categories'),
    path('tags/<str:tag>/', views.tag, name='tags'),
    path('search/', views.search, name='search'),
]
