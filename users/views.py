from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserCreateSerializer, UserAuthSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from users.models import CustomUser

def authorization_api_view(request):
    # validation
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # authentication
    CustomUser = authenticate(**serializer.validated_data)

    # if user exists return key else error
    if CustomUser:
        token, _ = Token.objects.get_or_create(user=CustomUser) #_ либо created
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)    

@api_view(['POST'])
def registration_api_view(request):
    # validation
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # recieve data
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']

    # create user
    user = CustomUser.objects.create_user(
        email=email,
        password=password,
        # is_active=False
        )   
    
    # created code (6-symbol)-> user

    # return response
    return Response(data={'user_id': user.id}, status=status.HTTP_201_CREATED)
    