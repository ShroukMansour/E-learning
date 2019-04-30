from django.urls import path

from company import views

app_name = 'vacancy'
urlpatterns = [
    path('vacancies/', views.VacancyList.as_view()),
    path('vacancies/<int:pk>/', views.VacancyDetail.as_view()),
    path('vacancies/apply/<int:vacancy_id>/', views.ApplyForVacancy.as_view()),
]