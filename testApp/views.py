from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework import authentication, permissions
import random
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.decorators import throttle_classes
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
from .models import AddDetailsModel, UserProductDetails
from .serializer import AddDetailsSerializer, AddDetailsSimpleSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# login
from django.contrib.auth import login, logout, authenticate


# throtling exmaples : OTP Generator
class OncePerDayUserThrottle(UserRateThrottle):
    rate = '5/min'


@api_view(['GET'])
@throttle_classes([OncePerDayUserThrottle])
def view(request):
    if request.method == "GET":
        return Response({"Message":  random.randint(1000, 9999)})
    return Response({"message": "oops! , you have reached your limits to genrate OTP ,see you tommorow MF"})


@api_view(["GET", "POST"])
@login_required
def add_details_view(request):
    if request.method == "POST":
        ser_data = AddDetailsSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response({"Message": ser_data.data})
        else:
            return Response({"Message": ser_data.errors})

    elif request.method == "GET":
        show_data = UserProductDetails.objects.all()
        print(request.user, request.auth)

        ser_data = AddDetailsSimpleSerializer(show_data, many=True)
        return Response({"Message": ser_data.data})


@api_view(["GET", "PATCH", "PUT", "PATCH", "DELETE"])
def edit_details(request, pk, format=None):
    if request.method == "GET":
        try:

            show_data = get_object_or_404(AddDetailsModel, pk=pk)
            ser_data = AddDetailsSerializer(show_data)
            print(request.auth)
            print(request.user)
            return Response(ser_data.data, status=status.HTTP_200_OK)
        except AddDetailsModel.DoesNotExist:
            return Response({"message": "No data"})

    if request.method == "DELETE":
        delete_data = AddDetailsModel.objects.get(pk=pk)
        delete_data.delete()
        return Response({"Message": "Succesfully deleted"})

    if request.method == "PUT":
        getId = get_object_or_404(AddDetailsModel, pk=pk)
        put_data = AddDetailsSerializer(getId, data=request.data)
        if put_data.is_valid():
            put_data.save()
            return Response({"Message": put_data.data})
        else:
            return Response({"Message": put_data.errors}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "PATCH":
        getID = get_object_or_404(AddDetailsModel, pk=pk)
        patch_ser = AddDetailsSerializer(
            getID, data=request.data, partial=True)
        if patch_ser.is_valid():
            patch_ser.save()
            return Response({"Message": "partially Updated Succes",
                             "data": patch_ser.data})
        else:

            return Response({"Message": "partially Updated Failed",
                             "data": patch_ser.errors})


@api_view(["GET", "POST"])
def search_detail(req):
    if req.method == "GET":
        search_query = req.GET.get("name")
        if search_query:
            get_detail = UserProductDetails.objects.filter(
                product_name__icontains=search_query)
            print("it work search")
            if not UserProductDetails.objects.filter(product_name__icontains=search_query).exists():
                print("No fdata")
                return Response({"message": "there is no data with the query "})

        else:
            return Response({"Message": "pls enter query/ No result "})

        ser_data = AddDetailsSimpleSerializer(get_detail, many=True)
        return Response(ser_data.data)


@api_view(["POST"])
@csrf_exempt
def login_view(req):
    if req.method == "POST":
        username = req.data.get("un")
        password = req.data.get("pd")
        print("username : ", username, "password :", password)
        user_auth = authenticate(username=username, password=password)
        if user_auth is not None:
            print("user_auth if works")
            login(req, user_auth)
            return Response({"Message": "Login successfull"})
        else:
            return Response({"message": "Login Failed"})
    return Response({"Msg": "NO login"})


@api_view(["POST"])
@login_required
@csrf_exempt
def logout_view(req):
    if req.method == "POST":
        req.user.auth_token.delete()
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& useer is  : ", req.user)
        return Response({"MSG": "Log out suceess"})
    return Response({"msg": "log out failed"})
