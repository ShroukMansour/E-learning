from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'quiz'

urlpatterns = format_suffix_patterns([
    # path('', views.index, name='index'),
    path('takeQuiz/<int:id>', views.QuizInstances.as_view()),
    path('score/<int:skill_type_id>', views.SkillScore.as_view()),
])