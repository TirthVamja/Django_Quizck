from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',views.dashboard,name='dashboard'),
    path('quiz',views.quiz,name='quiz'),
    path('createQuiz',views.createQuiz,name='createQuiz'),
    path('done',views.done,name='done'),
    path('stats/<int:pk>',views.stats,name="stats"),
    path('quizPage/<int:pk>',views.quizPage,name='quizPage'),
]