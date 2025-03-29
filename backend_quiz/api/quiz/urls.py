from api.quiz.views import answer, get_quiz
from django.urls import path

urlpatterns = [
    path('', get_quiz),
    path('answer', answer)
]
