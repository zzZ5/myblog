from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('articles/<int:id>/', views.article),
    path('categories/<str:category>/', views.category),
    path('tags/<str:tag>/', views.tag),
    path('search/', views.search),
]
