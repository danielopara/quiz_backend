import logging

from api.models import UserProfile
from api.serializers import UserProfileSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


class UserService:
    def create_user(self, request):
        try:
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            
            if User.objects.filter(username=username).exists():
                return Response({'error': "username already exists"}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=email).exists():
                return Response({'error': "email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.create_user(username=username, email=email, password=password)
            
            user_profile = UserProfile.objects.create(user=user)
            user_profile_serializer = UserProfileSerializer(user_profile)
            
            
            return Response({'message': "user created successfully", "data": user_profile_serializer.data}
                                 , status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def login(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            if not email or not password:
                return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

            # Find the user by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

            user = authenticate(username=user.username, password=password)

            if user is not None:
                refresh_token = RefreshToken.for_user(user)
                access_token = str(refresh_token.access_token)
                userProfile = UserProfile.objects.get(user=user)
                
                profile=UserProfileSerializer(userProfile)
                return Response({
                    'access_token': access_token,
                    'refresh_token': str(refresh_token),
                    'user': profile.data
                }, status=status.HTTP_200_OK)

            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
    
    def get_user(self, request):
        try:
            email = request.GET.get('email')
            allowed_queries = {"email"}
            
            if any(query not in allowed_queries for query in request.GET.keys()):
                return Response({'data': 'invalid query parameters'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                userProfile = UserProfile.objects.get(user__email=email)
                userprofile_serializer = UserProfileSerializer(userProfile)
                return Response({'message': 'user found', "data": userprofile_serializer.data}, status=status.HTTP_200_OK)
            except UserProfile.DoesNotExist:
                return Response({'message': 'user not found', 'data': email}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    def get_authorized_user(self, request):
        try:
            auth = JWTAuthentication()
            auth_result = auth.authenticate(request)
            
            if auth_result is None:
                return Response({"message": "no auth"}, status=status.HTTP_400_BAD_REQUEST)
            
            user, token = auth_result
            profile = UserProfile.objects.get(user=user)
            profile_serializer = UserProfileSerializer(profile)
            return Response({'message': 'user found', 'data': profile_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
