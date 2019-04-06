from django.urls import path

from company import views

app_name = 'vacancy'
urlpatterns = [
    path('vacancy/', views.VacancyList.as_view()),
    path('vacancy/<int:pk>/', views.VacancyDetail.as_view()),
]