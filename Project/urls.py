
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from quiz import views

router = routers.DefaultRouter()
router.register(r'questions', views.QuestionViewSet)
router.register(r'quizzes', views.QuizViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('quiz/', include('quiz.urls')),
    path('', include(router.urls)),
]
