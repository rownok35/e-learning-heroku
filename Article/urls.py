from django.urls import path
from Article import views

app_name = 'Article'

urlpatterns = [

    path('', views.article_list.as_view(), name='article_list'),
    path('write/', views.CreateArticle.as_view(), name='create_article'),
    path('details/<slug:slug>', views.article_details, name='article_details'),
    path('liked/<pk>/', views.liked, name='liked_post'),
    path('unliked/<pk>/', views.unliked, name='unliked_post'),
    path('my-articles/', views.MyArticles.as_view(), name='my_articles'),
    path('edit/<pk>/', views.UpdateArticle.as_view(), name='edit_article'),

]
