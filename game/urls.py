from django.urls import path
from . import views

urlpatterns = [
    path('fbase',views.fbase,name='fbase'),
    path('waiting',views.waiting,name="waiting"),
    path('showQuiz',views.showQuiz,name='showQuiz'),
    path('leaderboard',views.leaderboard,name='leaderboard'),
    path('download/<str:game>',views.download,name="download"),
    path('removed',views.removed,name="removed")
]