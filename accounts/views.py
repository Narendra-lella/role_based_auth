from django.shortcuts import render

from .serializers import MyTokenObtainpairserializer,Registrationserializer,LoginSerializer,UserListSerializer
from .models import Customuser


from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainpairserializer

class RegisterView(generics.CreateAPIView):

    queryset = Customuser.objects.all
    serializer_class = Registrationserializer
    permission_classes = (AllowAny,)

class LoginApiView(APIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        access = serializer.validated_data['access']
        refresh = serializer.validated_data['refresh']
        email = serializer.validated_data['email']
        role = serializer.validated_data['role']
        username = serializer.validated_data['username']
        

        status_code = status.HTTP_200_OK

        response = {
            'success': True,
            # 'statusCode': status_code,
            'message': 'User logged in successfully',
            'access': access,
            'refresh': refresh,
            # 'authenticatedUser': {
            #     'email': email,
            #     'username':username,
            #     'role': role
            # }
        }

        return Response(response, status=status_code)

class UsersListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Customuser.objects.all()