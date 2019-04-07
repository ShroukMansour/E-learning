from django.urls import path

from company import views

app_name = 'vacancy'
urlpatterns = [
    path('vacancies/', views.VacancyList.as_view()),
    path('vacancies/<int:pk>/', views.VacancyDetail.as_view()),
]