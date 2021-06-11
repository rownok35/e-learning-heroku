from django.urls import path
from ForumApp import views

app_name = 'ForumApp'

urlpatterns = [
    path('', views.ForumList.as_view(), name='forum_list'),
    path('create/', views.CreateForum.as_view(), name='create_forum'),
    path('my-problems/', views.MyProblems.as_view(), name='my-problems'),
    path('forum-details/<slug:slug>', views.forum_details, name='forum_details'),
    path('edit/<pk>/', views.UpdateForum.as_view(), name='edit_forum'),

]
