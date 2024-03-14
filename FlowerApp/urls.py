from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('order/', views.OrderView.as_view(), name='order'),
    path('catalog/', views.catalog, name='catalog'),
    path('consultation/', views.ConsultationRequestView.as_view(), name='consultation_request'),
    path('card/<int:bouquet_id>/', views.card, name='card'),
    path('quiz/', views.quiz, name='start_quiz'),
    path('quiz_step/', views.quiz_step, name='quiz_step'),
    path('result/', views.quiz_result, name='result')
]