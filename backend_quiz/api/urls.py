from django.urls import include, path

urlpatterns = [
    path('user/', include('api.user.urls')),
    path('quiz/', include('api.quiz.urls'))
]
