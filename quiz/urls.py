from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'quiz'

urlpatterns = format_suffix_patterns([
    # path('', views.index, name='index'),
    path('take/<int:quiz_id>', views.TakeQuiz.as_view()),
    path('submit/<int:quiz_instance_id>', views.SubmitQuiz.as_view()),
    path('score/<int:skill_type_id>', views.SkillScore.as_view()),
])