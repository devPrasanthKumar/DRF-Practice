from rest_framework import status
from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.contrib.auth.models import User

from rest_framework_simplejwt.tokens import RefreshToken
from JWTApp.models import ProductDetailsModel
from JWTApp.serializers import ProductSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class CreateAndListDataView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


# user regitser
class UserRegisterView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            serializer = UserSerializer(user)
            return Response({
                'access_token': str(access_token),
                'refresh_token': str(refresh),
                'success': "login sucess"

            }, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            print(refresh_token)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(refresh_token)
            print("error")

            return Response(status=status.HTTP_400_BAD_REQUEST)


class ProductDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):

        product_data = ProductDetailsModel.objects.filter(
            username=self.request.user)
        print(self.request.user)
        serializer = ProductSerializer(product_data, many=True)
        return Response(serializer.data)
