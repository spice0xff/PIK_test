from django.urls import path
from service_organizations import views


urlpatterns = [
    path('init_grid/', views.init_grid),
    path('coordinate_info/latitude=<str:latitude>&longitude=<str:longitude>/', views.coordinate_info),

    path('organisations/', views.OrganisationList.as_view()),
    path('organisation/<int:pk>/', views.OrganisationDetail.as_view()),

    path('services/', views.ServiceList.as_view()),
    path('service/<int:pk>/', views.ServiceDetail.as_view()),

    path('areas/', views.AreaList.as_view()),
    path('area/<int:pk>/', views.AreaDetail.as_view()),

    path('costs/', views.CostList.as_view()),
    path('cost/<int:pk>/', views.CostDetail.as_view()),
]
