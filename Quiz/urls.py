from django.urls import path
from Quiz import views

app_name = 'Quiz'

urlpatterns = [

    path('Create-Quiz/', views.Quiz_Form.as_view(), name='Quiz_Form'),
    path('my-quizzes/', views.MyQuizzes.as_view(), name='MyQuizzes'),
    path('', views.QuizList.as_view(), name='QuizList'),
    path('details/<pk>', views.quiz_details, name='quiz_details'),
    path('delete/<pk>', views.delete_quiz, name='delete_quiz'),
    path('delete-question/<pk>', views.delete_question, name='delete_question'),
    path('edit-question/<pk>', views.edit_question, name='edit_question'),
    path('test/<pk>', views.test, name='test'),
    path('test/<pk>/save/', views.save_quiz_view, name='save_view'),
]
