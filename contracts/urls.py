from django.urls import path
from . import views

app_name = 'contracts'
urlpatterns = [
    path('', views.index, name='index'),
    path('api/contracts/create/', views.ContractCreateAPIView.as_view(), name='contracts-create'),
    path('api/contracts/list/', views.ContractListAPIView.as_view(), name='contracts-list'),
    path('api/contracts/summary/', views.ContractSummaryAPIView.as_view(), name='contracts-summary'),
]