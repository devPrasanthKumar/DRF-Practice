from .models import ProductDetailsModel
from django.shortcuts import render

# importing User model
from django.contrib.auth.models import User

# importing Seriazler
from .serializers import ProductDetailsSerializer, UserAccountSerializer

# import CBV
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout, authenticate


class UserAccountView(APIView):

    # create a user account by POST method

    """ if request method is post ,it will work oherwise it wont work """

    def post(self, *args, **kwargs):

        # serailzer
        serializer = UserAccountSerializer(data=self.request.data)

        # it will  validate data
        if serializer.is_valid():
            user = serializer.save()

            """ 
            here, we want to genrate token automatically to user who creates(register) the account,
            it will genrate token automatically whenever new user create an account
            note : "token.key"  it has token 
            """
            token, created = Token.objects.get_or_create(user=user)

            # return the response
            return Response({"Reply": serializer.data,
                             "Token": token.key
                             })

        else:
            return Response({"Errors": serializer.errors})


# for user login
class UserAccountLoginView(APIView):
    def post(self, request):
        if request.method == "POST":

            """ get username and password """
            username = request.data.get("username")
            password = request.data.get("password")
            print(username, password)

            # authentiacte the request user
            auth = authenticate(username=username, password=password)

            token, created = Token.objects.get_or_create(user=auth)
            print(token.key)

            """ if user is valid .it will allow to login"""
            if auth is not None:
                # login
                login(self.request, auth)
                return Response({"Reply": "Login success"})
            else:
                return Response({"reply": "logged failed"})


class UserAccountLogoutView(APIView):
    def post(self, request):
        if request.method == "POST":

            """ it wll delete the request user's token  """
            self.request.user.auth_token.delete()
            print("Loggout success")
            return Response({"Message": "logged success"})


class ProductDetailsView(APIView):

    # it will allow only user is authenticated
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        print("my CURRENT USER IS :", request.user)
        if request.method == "GET":
            product_data = ProductDetailsModel.objects.filter(
                user_name=self.request.user)
            print(self.request.user)
            serializer = ProductDetailsSerializer(product_data, many=True)
            return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            serializer = ProductDetailsSerializer(
                data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
