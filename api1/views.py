from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import SignUpSerializer, Userserializer
from .tokens import create_jwt_pair_for_user
from drf_yasg.utils import swagger_auto_schema


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = []

    @swagger_auto_schema(operation_summary="Cria uma nova conta de  usuário",
                         operation_description="registra um novo usuário")
    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response = {"message": "User Created Successfully", "data": serializer.data}

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    permission_classes = []


    @swagger_auto_schema(operation_summary="Gera um token jwt",
                         operation_description="Login de usuário com email e senha")
    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:

            tokens = create_jwt_pair_for_user(user)

            response = {"message": "Login Successfull", "tokens": tokens}
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={"message": "Invalid email or password"})

    @swagger_auto_schema(operation_summary="Get request info",
                         operation_description="Mostra as informações da request do usuário")
    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth), "user.id":str(request.user.id)}

        return Response(data=content, status=status.HTTP_200_OK)
    

class UserView(APIView):    
   serializer_class = Userserializer
   def get(self, request):
        query = User.objects.all()
        query1 = query.user.id
        content = {"query": str(query), "query1": str(query1) }
        return Response(data=content , status=status.HTTP_200_OK)