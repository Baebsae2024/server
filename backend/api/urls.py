from django.urls import path
from .import views

urlpatterns = [
    path('',views.main),
    path('govern/', views.GovernAPI.as_view()),
    path('image/', views.ImageAPI.as_view()),
    path('caution/',views.CautionAPI.as_view()),
    # path('caution/info', views.CautionAPI.info),
    path('company/', views.CompanyAPI.as_view()),
]