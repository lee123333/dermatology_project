from django.urls import path
from . import views

urlpatterns = [
    path('', views.test),
    path('ajax_test/', views.ajax_test),
    path('ajax_find_alldata/', views.ajax_find_alldata),
    path('filter_web/', views.filter_web),
    path('ajax_filter_web/', views.ajax_filter_web),
    path('ajax_for_two_sig_detail/', views.ajax_for_two_sig_detail),
    path('ajax_for_one_sig_detail/', views.ajax_for_one_sig_detail),
]