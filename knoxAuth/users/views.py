
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import get_user_model
# Create your views here.
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import generics, permissions
from knox.models import AuthToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import NewUserSerializer   
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta
# Create your views here.
from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutView
from rest_framework.fields import empty
from rest_framework.views import APIView
from rest_framework import status
from .models import *
from details.models import Employee
from rest_framework import generics
from .serializers import *
from rest_framework.response import Response
from django.contrib.auth import SESSION_KEY, authenticate, login
from datetime import date, datetime
from datetime import datetime,timezone
from rest_framework import permissions
import string
import random


class CreateNewUser(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = NewUserSerializer

    def post(self, request, format=None):
        result = {}
        result['status'] = 'NOK'
        result['valid'] = False
        result["result"] = {'message': 'Unauthorized', 'data': []}
        if True:

            serializer = NewUserSerializer(data=request.data)
            if serializer.is_valid():

                try:
                    username = serializer.validated_data['email']
                    password = serializer.validated_data['password']

                    serializer.save()
                    name = request.data['name']
                    email = request.data['email']
                except:
                    result['status'] = 'NOK'
                    result['valid'] = False
                    # result['result']['message'] = "Error in sending mail"
                    return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

                result['status'] = 'OK'
                result['valid'] = True
                result['result']['message'] = "User created successfully !"
                return Response(result, status=status.HTTP_200_OK)
            else:
                result['result']['message'] = (list(serializer.errors.keys())[
                                                   0] + ' - ' + list(serializer.errors.values())[0][0]).capitalize()
                return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # return Response(result, status=status.HTTP_401_UNAUTHORIZED)

class Login(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        result = {}
        result['status'] = 'NOK'
        result['valid'] = False
        result['result'] = {"message": "Unauthorized access", "data": []}
        # print("jgjgj",request.data)

        if serializer.is_valid():
            try:
                user_data = authenticate(email=serializer.validated_data['email'],
                                         password=serializer.validated_data['password'])

            except:
                # Response data
                result['status'] = 'NOK'
                result['valid'] = False
                result['result']['message'] = 'User not present'
                # Response data
                return Response(result, status=status.HTTP_204_NO_CONTENT)

            if user_data is not None:
                user_details = CustomUser.objects.all().filter(email=user_data).values('id')
                                                                                #  'registered_on', 'emp_code',
                                                                                #  'current_status',
                                                                                #  'is_active')
                # print(user_details)
                if user_data.is_active:
                    login(request, user_data)
                    data = super(Login, self).post(request)
                    data = data.data
                    # print(data)
                    # data['message'] = "Login successfully"
                    data['user_info'] = user_details

                # Response data
                result['status'] = "OK"
                result['valid'] = True
                result['result']['message'] = "Login successfully"
                result['result']['data'] = data
                # result['result']['data'] = data
                # Response data
                return Response(result, status=status.HTTP_200_OK)
            else:

                # Response data
                result['status'] = "NOK"
                result['valid'] = False
                result['result']['message'] = 'Invalid Credentials'
                # Response data
                return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # Response data
        result['status'] = "NOK"
        result['valid'] = False
        result['result']['message'] = (
                    list(serializer.errors.keys())[0] + ' - ' + list(serializer.errors.values())[0][0]).capitalize()
        # Response data
        return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AllUsersSerializer


# class ActiveUserListView(APIView):
#     # permission_classes = [permissions.IsAuthenticated]
#     def get(self, request, format=None):
#         now = timezone.now()
#         cutoff_time = now - timedelta(minutes=request.session.get_expiry_age())
#         active_sessions = Session.objects.filter(expire_date__gte=cutoff_time)
#         user_ids = [int(session.get_decoded().get('_auth_user_id')) for session in active_sessions]
#         active_users = get_user_model().objects.filter(id__in=user_ids)

#         serializer = ActiveUserSerializer(active_users, many=True)
#         # if not serializer.data:
#         #     return Response({"message":"No active Users"}, status=status.HTTP_200_OK)

#         return Response(serializer.data, status=status.HTTP_200_OK)






# LOGOUT
class Logout(LogoutView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        print("gjgj")
        result = {}
        result['status'] = 'NOK'
        result['valid'] = False
        result['result'] = {"message": "Unauthorized access", "data": []}
        if request.user.is_authenticated:
            # print(request.data)
            try:
                request._auth.delete()
            except:
                # Response data
                result['status'] = "NOK"
                result['valid'] = False
                result['result']['message'] = 'Error while logging out'
                # Response data
                return Response(result, status=status.HTTP_200_OK)
            # Response data
            result['status'] = "OK"
            result['valid'] = True
            result['result']['message'] = 'Logout successfully in our function !'
            # Response data
            return Response(result, status=status.HTTP_200_OK)



class LogoutAllUsersView(APIView):
    # permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = LogoutAllSerializer

    def post(self, request, format=None):
        # print(request.headers)
        # User = get_user_model()  
        # User.objects.exclude(is_superuser=True).delete()
        # AuthToken.objects.all().delete()
        
        # return Response({"message": "All users have been deleted."}, status=status.HTTP_204_NO_CONTENT)
        user = request.user
        if user.id and user.is_staff==1:
            active_sessions = AuthToken.objects.all()
            # print("active sessions",active_sessions)
            for session in active_sessions:
                session.delete()
            return Response({"message": "All logged-in users have been deleted."}, status=status.HTTP_200_OK)
        return Response({"message": "Cannot delete logged-in users."}, status=status.HTTP_204_NO_CONTENT)


class LogoutAllView2(APIView):
    '''
    Log the user out of all sessions
    I.E. deletes all auth tokens for the user
    '''
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):

        user = request.user
        if user.id and user.is_staff==1:

            request.user.auth_token_set.all().delete()
            user_logged_out.send(sender=request.user.__class__,
                                request=request, user=request.user)
            return Response({"message":"Logged everyone out"}, status=status.HTTP_200_OK)
        return Response({"message":"Unauth user"}, status=status.HTTP_401_UNAUTHORIZED)
    

class IsLoggedIn(APIView):
    '''
    Log the user out of all sessions
    I.E. deletes all auth tokens for the user
    '''
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user
        if user.id:
            return Response({"message":"You r logged in"})
        return Response({"message":"Logged out ho"})
    
# class ChangePassword(APIView):

#     # serializer_class = ChangePasswordSerializer

#     def post(self, request, format=None):
#         if request.user.is_authenticated:
#             serializer = ChangePasswordSerializer(data=request.data)
#             if serializer.is_valid():
#                 user = request.user
#                 current_password = serializer.validated_data['current_password']

#                 if user.check_password(current_password):
#                     user.set_password(serializer.data['new_password'])
#                     user.save()
#                     return Response({'message':'password changed Successfuly'}, status=status.HTTP_200_OK)
#                 else:
#                     return Response({'error':'Entered Current Password is wrong'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
#         else:
#             return Response({'serializer.error'},status=status.HTTP_401_UNAUTHORIZED)
            


# class ResetPasswordLink(APIView):
#     # permission_classes = [IsAuthenticated]
#     serializer_class = ResetPasswordLinkSerializer

#     def post(self, request, format=None):
#         result = {}
#         result['status'] = "NOK"
#         result['valid'] = False
#         result['result'] = {"message": "Unauthorized access", "data": []}
#         key = ''.join(random.choices(
#             string.ascii_uppercase + string.digits, k=20))
#         serializer_data = dict()
#         serializer_data['key'] = key
#         serializer_data['time'] = datetime.now()

#         user_data = CustomUser.objects.all().filter(email=request.data['email'])

#         if len(user_data) == 0:
#             result['result']['message'] = 'Enter a valid email address.'
#             return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
#         else:
#             user_id = user_data.values()[0]['id']

#             try:
#                 prev_data = ResetPassword.objects.filter(user_id_id=user_id)
#                 len_prev = len(prev_data.values())

#             except:
#                 pass

#             if len_prev > 0:

#                 serializer_data = {}
#                 serializer_data['key'] = key
#                 serializer_data['time'] = datetime.now()
#                 # serializer_data['user_id']  = user_id
#                 serializer = ResetPasswordLinkSerializer(ResetPassword.objects.get(
#                     user_id_id=user_id), data=serializer_data, partial=True)

#                 if serializer.is_valid():
#                     serializer.save()
#                 else:
#                     result['result']['message'] = (
#                                 list(serializer.errors.keys())[0] + ' - ' + list(serializer.errors.values())[0][
#                             0]).capitalize()
#                     return Response(result, status=status.HTTP_200_OK)

#             else:

#                 serializer_data = {}
#                 serializer_data['key'] = key
#                 serializer_data['time'] = datetime.now()
#                 serializer_data['user_id'] = user_id

#                 serializer = ResetPasswordLinkSerializer(data=serializer_data)

#                 if serializer.is_valid():
#                     serializer.save()
#                 else:
#                     result['result']['message'] = (
#                                 list(serializer.errors.keys())[0] + ' - ' + list(serializer.errors.values())[0][
#                             0]).capitalize()
#                     return Response(result, status=status.HTTP_200_OK)

#         try:
#             # data = "https://sorasorimukhyomontri.com/ssm-dashboard/auth/password/create/" + key
#             data = "http://localhost:8000/newpass/" + key
#             email = request.data['email']
#             obj = CustomUser.objects.filter(email=email).values()
#             obj = obj[0]['name']
#             msg_plain = ''
#             msg_html = render_to_string(
#                 'users/resetpass.html', {'link': data, 'obj': obj})

#             # msg_html = f"Hi a reset request has been raised by you  {'link': data, 'obj': obj})"
#             # msg_html = "Hi a reset request has been raised by you"

#             # send_mail('Reset Password request', msg_plain, 'info@sorasorimukhyomontri.com',
#             #           [request.data['email']], html_message=msg_html, )
#             send_mail('Reset Password request', msg_plain, 'nutansingh4518@gmail.com',
#                       [request.data['email']], html_message=msg_html, )
#         except:
#             result['result']['message'] = "Error while sending mail"
#             return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         # Response data
#         result['status'] = "OK"
#         result['valid'] = True
#         result['result']['message'] = "Reset password link has been sent to your mail address"
#         # Response data

#         return Response(result, status=status.HTTP_200_OK)
# class ChangePassword(APIView):
#     def post(self, request, format=None):
#         try:
#             obj = CustomUser.objects.get(token = request.data['token'])
#             print(obj)
#         except Exception as e:
#             print(e)
#         return render(request,'change-password.html')

# class ForgotPassword(APIView):
#     def post(self, request, format=None):
#         try:
#             email = request.POST.get('email')
#             if not CustomUser.objects.filter(email = email).first():
#                 return Response(request,'No user found with this email')
#             token = ''.join(random.choices(
#             string.ascii_uppercase + string.digits, k=20))
#             data = "http://localhost:8000/newpass/" + token
#             email = request.data['email']
#             obj = CustomUser.objects.filter(email=email).values()
#             obj = obj[0]['name']
#             msg_plain = ' the reset is link is here'
#             msg_html = render_to_string(
#                 'resetpass.html', {'link': data, 'obj': obj})
#             email_from = settings.EMAIL_HOST_USER
#             recipient_list =request.data['email']


#             send_mail('Reset Password request', msg_plain, email_from,
#                       [recipient_list] )
#             return Response({'message':'An email has been sent'}, status=status.HTTP_200_OK)
#             # send_mail('Reset Password request', msg_plain, 'nutansingh4518@gmail.com',
#             #           [request.data['email']], html_message=msg_html, )
#             # obj = CustomUser.objects.get(email = email) 
#         except Exception as e:
#             print(e)
#         return render(request,'reset.html')





class ChangePassword(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request, format=None):
        result = {}
        result['status'] = "NOK"
        result['valid'] = False
        result['result'] = {"message": "Unauthorized access", "data": []}

        if request.user.is_authenticated:

            if request.user.is_anonymous:
                result['result']['message'] = "User Invalid"
                return Response(result, status=status.HTTP_200_OK)

            serializer = ChangePasswordSerializer(data=request.data)
            if serializer.is_valid():
                user = request.user

                if user.check_password(serializer.data['old_password']):
                    new_password = serializer.data['new_password']
                    user.set_password(serializer.data['new_password'])
                    request.user.save()

                    # Response data
                    result['status'] = "OK"
                    result['valid'] = True
                    result['result']['message'] = "Password Changed"
                    # Response data
                    return Response(result, status=status.HTTP_201_CREATED)
                else:
                    result['result']['message'] = "Pasword did not match"
                    return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class ResetPasswordLink(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ResetPasswordLinkSerializer

    def post(self, request, format=None):
        result = {}
        result['status'] = "NOK"
        result['valid'] = False
        result['result'] = {"message": "Unauthorized access", "data": []}
        key = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=20))
        serializer_data = dict()
        serializer_data['key'] = key
        serializer_data['time'] = datetime.now()
        print("generated Key ::::::::",key)
        user_data = CustomUser.objects.all().filter(email=request.data['email'])
        print("user_data:::",user_data[0])
        len_prev = 0
        if len(user_data) == 0:
            result['result']['message'] = 'Enter a valid email address.'
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            user_id = user_data.values()[0]['id']
            print("user_id",user_id)
            try:
                prev_data = ResetPassword.objects.filter(user_id_id=user_id)
                len_prev = len(prev_data.values())

            except:
                pass

            if len_prev > 0:

                serializer_data = {}
                serializer_data['key'] = key
                serializer_data['time'] = datetime.now()
                # serializer_data['user_id']  = user_id
                serializer = ResetPasswordLinkSerializer(ResetPassword.objects.get(
                    user_id_id=user_id), data=serializer_data, partial=True)

                if serializer.is_valid():
                    serializer.save()
                else:
                    result['result']['message'] = (
                                list(serializer.errors.keys())[0] + ' - ' + list(serializer.errors.values())[0][
                            0]).capitalize()
                    return Response(result, status=status.HTTP_200_OK)

            else:

                serializer_data = {}
                serializer_data['key'] = key
                serializer_data['time'] = datetime.now()
                serializer_data['user_id'] = user_id

                serializer = ResetPasswordLinkSerializer(data=serializer_data)

                if serializer.is_valid():
                    serializer.save()
                else:
                    result['result']['message'] = (
                                list(serializer.errors.keys())[0] + ' - ' + list(serializer.errors.values())[0][
                            0]).capitalize()
                    return Response(result, status=status.HTTP_200_OK)

        try:
            # data = "https://sorasorimukhyomontri.com/ssm-dashboard/auth/password/create/" + key
            # data = "https://youthclub.pkconnect.com/stage/crm_dashboard/auth/password/create/" + key
            data = "file:///C:/Users/nutan/OneDrive/Desktop/django/SuperUserKnoxAutnetication/knoxAuth/templates/users/newpass.html/" + key


            email = request.data['email']
            obj = CustomUser.objects.filter(email=email).values()
            # print("obj1:::",obj)

            obj = obj[0]['name']

            # print("obj2:::",obj)
            msg_plain = ''
            msg_html = f"Hi {obj} to Reset your password you need to click on this link {data}"
            send_mail('Reset Password request', msg_plain, 'nutansingh4518@gmail.com',
                      [request.data['email']], html_message=msg_html, )
        except:
            result['result']['message'] = "Error while sending mail"
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # Response data
        result['status'] = "OK"
        result['valid'] = True
        
        result['result']['message'] = "Reset password link has been sent to your mail address"
        result['data'] = data
        return Response(result, status=status.HTTP_200_OK)

class UserResetPassword(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ResetPasswordsSerializer

    def post(self, request, format=None):
        result = {}
        result['status'] = "NOK"
        result['valid'] = False
        result['result'] = {"message": "Unauthorized access", "data": []}
        if request.data['password'] != request.data['confirm_password']:
            result['result']['message'] = "Both passwords must be same"
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        try:
            user_details = ResetPassword.objects.filter(key=request.data['key']).values('id', 'key', 'time',
                                                                                        'user_id_id__email',
                                                                                        'user_id_id')
            if len(user_details) == 0:
                result['result']['message'] = "Invalid user"
                return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            pass

        email_id = user_details[0]['user_id_id__email']
        # start_time = user_details[0]['time']
        # endtime = datetime.now()
        # duration = (endtime - start_time).total_seconds() / 60.0
        
        # endtime = datetime(2023, 8, 30, 12, 0, 0, tzinfo=timezone.utc)
        # start_time_aware = datetime(2023, 8, 30, 10, 0, 0, tzinfo=timezone.utc)
        # duration = (endtime - start_time_aware).total_seconds() / 60.0

        # if duration > 20:
        #     result['status'] = "OK"
        #     result['valid'] = True
        #     result['result']['message'] = "Request Time Out!"
        #     return Response(result, status=status.HTTP_408_REQUEST_TIMEOUT)

        serializer = ResetPasswordsSerializer(data=request.data)

        try:
            user = CustomUser.objects.get(email=email_id)
        except:
            result['result']['message'] = "Invalid Email Address"
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            obj = CustomUser.objects.filter(email=email_id).values()
            obj = obj[0]['name']
            msg_plain = ''
            # msg_html = render_to_string('users/reset.html', {'name': obj})
            msg_html = f"Hi {obj} your password has been reset successfuly"

            # send_mail('Password Reset  Sucessful', msg_plain,
            #           'nutansingh4518@gmail.com', [email_id], html_message=msg_html, )
            
            send_mail('Password Reset  Sucessful', msg_plain, 'nutansingh4518@gmail.com',
                      [email_id], html_message=msg_html, )
            prev_data = ResetPassword.objects.get(id=user_details[0]['id'])

            serializer_data = {}
            serializer_data['key'] = ""
            serializer = ResetPasswordLinkSerializer(
                prev_data, data=serializer_data, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                result['status'] = "NOK"
                result['valid'] = False
                result['result']['message'] = (
                            list(serializer.errors.keys())[0] + ' - ' + list(serializer.errors.values())[0][
                        0]).capitalize()
                return Response(result, status=status.HTTP_200_OK)

            # Response data
            result['status'] = "OK"
            result['valid'] = True
            result['result']['message'] = "Password reset successfully !"
            # Response data
            return Response(result, status=status.HTTP_200_OK)
        else:
            result['result']['message'] = (
                        list(serializer.errors.keys())[0] + ' - ' + list(serializer.errors.values())[0][0]).capitalize()
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
