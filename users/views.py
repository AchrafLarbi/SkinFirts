from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework import status
from users.tokens import create_jwt_pair_for_user
from .models import User
from .serializers import UserSerializer, NewPasswordSerializer
from rest_framework.views import APIView
from rest_framework.request import Request
from django.contrib.auth import authenticate, update_session_auth_hash
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
import random
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken
from .serializers import PasswordResetRequestSerializer, PasswordResetSerializer
from django.conf import settings

def generate_otp():
    number_list = [x for x in range(10)]  # Use of list comprehension
    code_items_for_otp = []

    for i in range(6):
        num = random.choice(number_list)
        code_items_for_otp.append(num)

    code_string = "".join(str(item) for item in code_items_for_otp)
    return code_string


class ListCreateUser(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            success_response = {
                "status": status.HTTP_201_CREATED,
                "message": "User created successfully"
            }
            return Response(success_response, status=status.HTTP_201_CREATED)
        else:
            error_messages = []
            for field, errors in serializer.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            error_message_str = " ".join(error_messages)
            
            error_response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "errorMessage": error_message_str
            }
            return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email = email,password= password)

        if user is not None:
            tokens = create_jwt_pair_for_user(user)

            response = {"message": "Login Succesfull", "token": tokens}#,"id":user.id
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            error_response = {
                "status": status.HTTP_401_UNAUTHORIZED,
                "errorMessage": "Invalid email or password"
            }
            return Response(data=error_response, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request: Request):
        content = {"user": str(request.user),"auth": str(request.auth)}

        return Response(data=content, status=status.HTTP_200_OK)
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    
    

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = NewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.data.get('old_password')
            new_password = serializer.data.get('new_password')

            # Check if the old password is correct
            if not user.check_password(old_password):
                error_response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "errorMessage": "Incorrect old password."
                }

                return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)

            # Set the new password
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user) #bach user mydirch login again

            return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        
        else:
            error_messages = []
            for field, errors in serializer.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            error_message_str = " ".join(error_messages)
            
            error_response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "errorMessage": error_message_str
            }
            return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                if user.otp is None:
                    user.save()

                subject = 'Password Reset Request'
                message = f'Here is the message with {user.otp}.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
                send_mail(subject, message, email_from, recipient_list, fail_silently=False)
                return Response({'message': 'Password reset OTP sent'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                error_response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "errorMessage": "Invalid email address"
                }
                return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)
        else:
            error_messages = []
            for field, errors in serializer.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            error_message_str = " ".join(error_messages)
            
            error_response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "errorMessage": error_message_str
            }
            return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)
        
class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']
            try:
                user = User.objects.get(otp=otp)
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                error_response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "errorMessage": "Invalid OTP"
                }
                return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)
        else:
            error_messages = []
            for field, errors in serializer.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            error_message_str = " ".join(error_messages)
            
            error_response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "errorMessage": error_message_str
            }
            return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)



# class PasswordResetRequestView(APIView):
#     def post(self, request):
#         serializer = PasswordResetRequestSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             try:
#                 user = User.objects.get(email=email)
#                 token = RefreshToken.for_user(user).access_token
#                 reset_url = f'{request.build_absolute_uri(reverse("password-reset-confirm"))}?token={token}'

#                 subject = 'Password Reset Request'
#                 message = f"Click the link to reset your password: {reset_url}" 
#                 email_from = settings.EMAIL_HOST_USER
#                 recipient_list = [email ]
    
#                 send_mail( subject, message, email_from, recipient_list, fail_silently = False)
#                 return Response({'message': 'Password reset link sent'}, status=status.HTTP_200_OK)
#             except User.DoesNotExist:
#                 error_response = {
#                     "status": status.HTTP_400_BAD_REQUEST,
#                     "errorMessage": "Invalid email address"
#                 }
#                 return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             error_messages = []
#             for field, errors in serializer.errors.items():
#                 for error in errors:
#                     error_messages.append(f"{field}: {error}")
#             error_message_str = " ".join(error_messages)
            
#             error_response = {
#                 "status": status.HTTP_400_BAD_REQUEST,
#                 "errorMessage": error_message_str
#             }
#             return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)
                
        



# class PasswordResetConfirmView(APIView):
#     def post(self, request):
#         token = request.query_params.get('token')
#         serializer = PasswordResetSerializer(data={**request.data, 'token': token})
#         if serializer.is_valid():
#             try:
#                 UntypedToken(token)
#                 user_id = UntypedToken(token).payload['user_id']
#                 user = User.objects.get(id=user_id)
#                 user.set_password(serializer.validated_data['new_password'])
#                 user.save()
#                 return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
#             except Exception as e:
#                 error_response = {
#                     "status": status.HTTP_400_BAD_REQUEST,
#                     "errorMessage": "Invalid token"
#                 }
#                 return Response(data=error_response ,status=status.HTTP_400_BAD_REQUEST)
#         else:
#             error_messages = []
#             for field, errors in serializer.errors.items():
#                 for error in errors:
#                     error_messages.append(f"{field}: {error}")
#             error_message_str = " ".join(error_messages)
            
#             error_response = {
#                 "status": status.HTTP_400_BAD_REQUEST,
#                 "errorMessage": error_message_str
#             }
#             return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)