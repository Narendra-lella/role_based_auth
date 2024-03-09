from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token,RefreshToken,AccessToken
from django.contrib.auth.models import update_last_login
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate

from .models import Customuser

class MyTokenObtainpairserializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token =  super().get_token(user)
    
        token['username'] = user.username
        token['email'] = user.email 
        token['role'] = user.role

        return token
    
class Registrationserializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True,validators=[validate_password])
    password2 = serializers.CharField(write_only = True,required=True)
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=Customuser.objects.all())])

    class Meta:
        model = Customuser
        fields = '__all__'
    
    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password':"password Fields didn't matched"}
            )
        if attrs['username'] == None:
            raise serializers.ValidationError(
                {"username":"Username is required"}
            )
        return attrs
    def create(self, validated_data):
        user = Customuser.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            dob=validated_data['dob'],
            role = validated_data['role']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=20,write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def validate(self,data):
        email = data['email']
        passowrd = data['password']
        user = authenticate(email=email,password=passowrd)
        if user is None:
            raise serializers.ValidationError(
                {"Invalied Credentials"}
            )
        try :
            token_serializer = MyTokenObtainpairserializer()
            tokens = token_serializer.get_token(user)
            refresh_token = str(RefreshToken.for_user(user))
            access_token = str(tokens.access_token)


            update_last_login(None,user)

            validation = {
                'access' : access_token,
                'refresh' : refresh_token,
                'email':user.email,
                'username':user.username,
                'role':user.role
            }

            return validation
        except Customuser.DoesNotExist:
            raise serializers.ValidationError({"invalied Credentials"})


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = ('username', 'email', 'role')