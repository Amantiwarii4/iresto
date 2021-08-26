import random
import string
from django.shortcuts import render
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, BannerSerializer, CategorySerializer, \
    UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from rest_framework import generics, status
from .models import Banner, Category
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def add_banner(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category_name = request.POST.get('category_name')
        # created_at = request.POST.get('created_at')
        image = request.FILES["image"]
        banner_serializer = BannerSerializer(data=request.POST)
        if banner_serializer.is_valid():
            banner = Banner.objects.create(title=title, category_name=category_name, image=image)
            return JsonResponse({'message': 'Banner Created Sucessfully!', 'data': banner_serializer.data},
                                status=status.HTTP_201_CREATED)
    return JsonResponse(banner_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        discription = request.POST.get('discription')
        # created_at = request.POST.get('created_at')
        image = request.FILES["image"]
        category_serializer = CategorySerializer(data=request.POST)
        if category_serializer.is_valid():
            banner = Category.objects.create(name=name, discription=discription, image=image)
            return JsonResponse({'message': 'Banner Created Sucessfully!', 'data': category_serializer.data},
                                status=status.HTTP_201_CREATED)
        return JsonResponse(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def category_list(request):
    if request.method == 'GET':
        category = Category.objects.all()
        category_serializer = CategorySerializer(category, many=True)
        return JsonResponse({'message': 'Category listed successfully!', 'data': category_serializer.data}, safe=False)
        # 'safe=False' for objects serialization


@csrf_exempt
def category_edit(request, pk):
    if request.method == 'POST':
        name = request.POST.get('name')
        discription = request.POST.get('discription')
        # created_at = request.POST.get('created_at')
        image = request.FILES["image"]
        category_serializer = CategorySerializer(data=request.POST)
        if category_serializer.is_valid():
            category = Category.objects.filter(id=pk).update(name=name, discription=discription, image=image)
            users = Category.objects.get(id=pk)
            category = CategorySerializer(users)
            return JsonResponse({'message': 'Category update successfully!', 'data': category_serializer.data},
                                status=status.HTTP_201_CREATED)
        return JsonResponse(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        # logged in using username and password
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # users = authenticate(username=username , password = password)

        # logged in using phone
        phone = request.POST.get('phone')
        try:
            users = User.objects.get(phone=phone)
        except:
            users = None
        if users is not None:
            users_serializer = UserSerializer(users)
            return JsonResponse({'message': 'User logged in successfully!', 'data': users_serializer.data,
                                 'otp': random.randint(1111, 9999)}, status=status.HTTP_204_NO_CONTENT)
        else:
            S = 10
            username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
            # print(username)
            # exit()
            user = User.objects.create_user(username=str(username),
                                            password="herk12354312",
                                            phone=phone,
                                            )
            user.save()
            id1 = user.id
            users = User.objects.get(id=id1)
            users_serializer = UserSerializer(users)
            return JsonResponse({'message': 'User logged in successfully!', 'data': users_serializer.data,
                                 'otp': random.randint(1111, 9999)}, status=status.HTTP_204_NO_CONTENT)


# extra code for login and register
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


from django.contrib.auth.models import User

from rest_framework import generics


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyotp
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import phoneModel
import base64


# This class returns the string needed to generate the key
class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"


class getPhoneNumberRegistered(APIView):
    # Get to Create a call for OTP
    @staticmethod
    def get(request, phone):
        try:
            Mobile = phoneModel.objects.get(Mobile=phone)  # if Mobile already exists the take this else create New One
        except ObjectDoesNotExist:
            phoneModel.objects.create(
                Mobile=phone,
            )
            Mobile = phoneModel.objects.get(Mobile=phone)  # user Newly created Model
        Mobile.counter += 1  # Update Counter At every Call
        Mobile.save()  # Save the data
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Key is generated
        OTP = pyotp.HOTP(key)  # HOTP Model for OTP is created
        print(OTP.at(Mobile.counter))
        # Using Multi-Threading send the OTP Using Messaging Services like Twilio or Fast2sms
        return Response({"OTP": OTP.at(Mobile.counter)}, status=200)  # Just for demonstration

    # This Method verifies the OTP
    @staticmethod
    def post(request, phone):
        try:
            Mobile = phoneModel.objects.get(Mobile=phone)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)  # False Call

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Generating Key
        OTP = pyotp.HOTP(key)  # HOTP Model
        if OTP.verify(request.data["otp"], Mobile.counter):  # Verifying the OTP
            Mobile.isVerified = True
            Mobile.save()
            return Response("You are authorised", status=200)
        return Response("OTP is wrong", status=400)


# Time after which OTP will expire
EXPIRY_TIME = 50  # seconds


class getPhoneNumberRegistered_TimeBased(APIView):
    # Get to Create a call for OTP
    @staticmethod
    def get(request, phone):
        try:
            Mobile = phoneModel.objects.get(Mobile=phone)  # if Mobile already exists the take this else create New One
        except ObjectDoesNotExist:
            phoneModel.objects.create(
                Mobile=phone,
            )
            Mobile = phoneModel.objects.get(Mobile=phone)  # user Newly created Model
        Mobile.save()  # Save the data
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Key is generated
        OTP = pyotp.TOTP(key, interval=EXPIRY_TIME)  # TOTP Model for OTP is created
        print(OTP.now())
        # Using Multi-Threading send the OTP Using Messaging Services like Twilio or Fast2sms
        return Response({"OTP": OTP.now()}, status=200)  # Just for demonstration

    # This Method verifies the OTP
    @staticmethod
    def post(request, phone):
        try:
            Mobile = phoneModel.objects.get(Mobile=phone)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)  # False Call

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Generating Key
        OTP = pyotp.TOTP(key, interval=EXPIRY_TIME)  # TOTP Model
        if OTP.verify(request.data["otp"]):  # Verifying the OTP
            Mobile.isVerified = True
            Mobile.save()
            return Response("You are authorised", status=200)
        return Response("OTP is wrong/expired", status=400)
