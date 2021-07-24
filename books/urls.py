from os import name
from django.urls import path, include
from .import views
urlpatterns = [
    path('', views.display_charts, name='index'),
    path('filters', views.filter_options,name='filter_options'),
    path('annual/<int:year>/sales', views.get_annual_sales, name='annual_chart'),
    path('payment-success/<int:year>/', views.payment_success_chart, name='chart-payment-success'),
    path('payment-method/<int:year>/', views.payment_method_chart, name='chart-payment-method'),
     path('spend-per-customer/<int:year>/', views.spend_per_customer_chart, name='chart-spend-per-customer'),
]
