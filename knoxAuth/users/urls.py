from django.urls import path, include
from knox import views as knox_views
from .views import *

app_name = 'users'  # Add this line to set the app name

urlpatterns = [
    path('allUsers/', UserListView.as_view(), name='abc'),
    path('register/', CreateNewUser.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('logoutall/', LogoutAllUsersView.as_view(), name='logout2'),
    path('islogin/', IsLoggedIn.as_view(), name='islogin'),
    # path('changepassword/', ChangePassword.as_view(), name='ChangePassword'),
    # path('forgotpassword/',ForgotPassword.as_view(),name='resetpasswordlink'),
    # path('changepassword/',ChangePassword.as_view(),name='resetpassword'),
    path('changepassword/',ChangePassword.as_view()),
    path('resetpasswordlink/',ResetPasswordLink.as_view()),
    path('resetpassword/',UserResetPassword.as_view()),

    # path('password_reset/',include('django_rest_passwordreset.urls', namespace='password_reset')),



]
