from django.urls import path,include
from . import views
from knox import views as knox_views
from .views import *
urlpatterns = [
 
   
    path('new/',views.NewEmployeeAPI.as_view()),
    path('all/',ListEmployeeAPIView.as_view()),
    path('updateE/<int:pk>/',UpdateEmployeeAPI.as_view()),
    path('deleteE/<int:pk>/',views.DeleteEmployeeAPIView.as_view()),

   

]
