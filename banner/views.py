import json
import random
import string
from itertools import count
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, BannerSerializer, CategorySerializer, \
    UserSerializer, AdminSerializer, UserupdateSerializer, BannerclientSerializer, ProductSerializer, CartSerializer, \
    OrdersSerializer, OfferSerializer, AddressSerializer, CategoryadminSerializer, DieninSerializer, BookingSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from rest_framework import generics, status
from .models import Banner, Category, Products, Product_image, Cart, Orders, Offers, Address, Dine_in, Booking, Review
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from django.contrib.auth.hashers import make_password, check_password
import binascii
import base64
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.authentication import get_authorization_header
from rest_framework import HTTP_HEADER_ENCODING


def authorized(request):
    auth = get_authorization_header(request).split()
    if not auth or auth[0].lower() != b'basic':
        msg = _("Not basic authentication.")
        result = {'status': False, 'message': msg}
        return result
    if len(auth) == 1:
        msg = _('Invalid basic header. No credentials provided.')
        result = {'status': False, 'message': msg}
        return result
    elif len(auth) > 2:
        msg = _('Invalid basic header. Credentials string should not contain spaces.')
        result = {'status': False, 'message': msg}
        return result
    try:
        auth_parts = base64.b64decode(auth[1]).decode(HTTP_HEADER_ENCODING).partition(':')
    except (TypeError, UnicodeDecodeError, binascii.Error):
        msg = _('Invalid basic header. Credentials not correctly base64 encoded.')
        result = {'status': False, 'message': msg}
        return result

    userid, password = auth_parts[0], auth_parts[2]
    # Your auth table specific codes
    if 'iresto' == userid and '026866326a9d1d2b23226e4e8929192g' == password:  # my dummy code
        result = {'status': True, 'message': ""}
        return result
    else:
        msg = _('User not found.')
        result = {'status': False, 'message': msg}
        return result


@csrf_exempt
def add_banner(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category_name = request.POST.get('category_name')
        image = request.FILES["image"]
        banner_serializer = BannerSerializer(data=request.POST)
        if banner_serializer.is_valid():
            banner = Banner.objects.create(title=title, category_name=category_name, image=image)
            return JsonResponse({'message': 'Banner Created Sucessfully!', 'data': banner_serializer.data}
                                )
    return JsonResponse(banner_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def banner_list(request):
    if request.method == 'GET':
        banner = Banner.objects.all()
        banner_serializer = BannerSerializer(banner, many=True)
        return JsonResponse({'message': 'Banner listed successfully!', 'data': banner_serializer.data}, safe=False)
        # 'safe=False' for objects serialization


def banner_list_client(request):
    result = authorized(request)
    if result['status'] == True:
        if request.method == 'GET':
            banner = Banner.objects.all()
            banner_serializer = BannerclientSerializer(banner, many=True)
            return JsonResponse({'message': 'Banner listed successfully!', 'data': banner_serializer.data}, safe=False)
    return JsonResponse({"message": "Unauthorised User", })


@csrf_exempt
def banner_edit(request, pk):
    if request.method == 'POST':
        title = request.POST.get('title')
        category_name = request.POST.get('category_name')
        image = request.FILES["image"]
        banner_serializer = BannerSerializer(data=request.POST)
        if banner_serializer.is_valid():
            banner = Banner.objects.filter(id=pk).update(title=title, category_name=category_name)
            banner = Banner.objects.get(id=pk)
            banner.image = image
            banner.save()
            return JsonResponse({'message': 'Banner update successfully!', 'data': banner_serializer.data}
                                )
        return JsonResponse(banner_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def banner_delete(request, pk):
    if request.method == 'POST':
        users = Banner.objects.filter(id=pk).delete()
        return JsonResponse({'message': 'Banner deleted successfully!'})


@csrf_exempt
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        discription = request.POST.get('discription')
        # created_at = request.POST.get('created_at')
        image = request.FILES["image"]
        category_serializer = CategorySerializer(data=request.POST)
        if category_serializer.is_valid():
            banner = Category.objects.create(category_name=name, discription=discription, image=image)
            return JsonResponse({'message': 'Category Created Sucessfully!', 'data': category_serializer.data},
                                status=status.HTTP_201_CREATED)
        return JsonResponse(category_serializer.errors)


def category_list(request):
    result = authorized(request)
    if result['status'] == True:
        if request.method == 'GET':
            category = Category.objects.all()
            category_serializer = CategorySerializer(category, many=True)
            return JsonResponse({'message': 'Category listed successfully!', 'data': category_serializer.data},
                                safe=False)
        # 'safe=False' for objects serialization
    return JsonResponse({'message': 'Unauthorised User', })


@csrf_exempt
def show_category(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        try:
            # token = request.POST.get('token')
            user = User.objects.get(token=token)
        except:
            user = None
        if user is not None:
            category = Category.objects.all()
            category_serializer = CategoryadminSerializer(category, many=True)
            return JsonResponse({'Status': True, 'data': category_serializer.data, }, safe=False)
    return JsonResponse({'Status': False, })


@csrf_exempt
def category_edit(request, pk):
    if request.method == 'POST':
        name = request.POST.get('name')
        discription = request.POST.get('discription')
        # created_at = request.POST.get('created_at')
        image = request.FILES["image"]
        category_serializer = CategorySerializer(data=request.POST)
        if category_serializer.is_valid():
            category = Category.objects.filter(id=pk).update(name=name, discription=discription)
            users = Category.objects.get(id=pk)
            users.image = image
            users.save()
            category = CategorySerializer(users)
            return JsonResponse({'message': 'Category update successfully!', 'data': category_serializer.data}
                                )
        return JsonResponse(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def category_delete(request):
    if request.method == 'POST':
        pk = request.POST.get('id')
        try:
            users = Category.objects.get(id=pk)
            users.delete()
            return JsonResponse({'Status': True, 'message': 'Category deleted successfully!'})
        except:
            return JsonResponse({'Status': False, 'message': 'Id not found!'})


@csrf_exempt
def user_login(request):
    result = authorized(request)
    if result['status'] == True:
        tok = MyTokenObtainPairSerializer()  # object to get user token
        if request.method == 'POST':
            phone = request.POST.get('phone')
            block = User.objects.filter(phone=phone).values('is_block')
            try:
                users = User.objects.get(phone=phone)
                id = User.objects.filter(phone=phone).values('id')
                block = User.objects.filter(phone=phone).values('is_block')
                block1 = block[0]
            except:
                users = None
            if users is not None and block1['is_block'] == False:
                users_serializer = UserSerializer(users)
                token = tok.get_token(users)
                otp = random.randint(1111, 9999)
                id1 = id[0]
                otp_entry = User.objects.filter(id=id1['id']).update(otp=otp)
                return JsonResponse(
                    {'message': 'User logged in successfully!', 'data': users_serializer.data,
                     'otp': otp})
            else:
                S = 10
                username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
                otp = random.randint(1111, 9999)
                try:
                    user = User.objects.create_user(username=str(username),
                                                    password="herk12354312",
                                                    phone=phone,
                                                    otp=otp,
                                                    )
                    user.save()
                    id1 = user.id
                    users = User.objects.get(id=id1)
                    token = tok.get_token(users)
                    stoken = str(token)
                    users_serializer = UserSerializer(users)
                    return JsonResponse(
                        {'message': 'User logged in successfully!', 'data': users_serializer.data,
                         'otp': otp})
                except:
                    return JsonResponse(
                        {'message': 'You have been blocked by admin', })
    return JsonResponse({'message': 'Unauthorised User', })


# @api_view(["POST"])
@csrf_exempt
def add_products(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            category_name = request.POST.get('category_name')
            discription = request.POST.get('discription')
            price = request.POST.get('price')
            fav = request.POST.get('fav')
            feature_image = request.FILES['feature_image']
            unit = request.POST.get('unit')
            variation1 = request.POST.get('variation')
            unit_price1 = request.POST.get('unit_price')
            category = Category.objects.get(id=category_name)
            if ',' not in str(variation1) and ',' not in str(unit_price1):
                str(variation1) + ','
                str(unit_price1) + ','
            variation2 = variation1.split(',')
            unit_price3 = unit_price1.split(',')
            type = request.POST.get('type')
            unit_price = []
            for i in range(0, len(variation2)):
                unit_price2 = {'id': i, 'size': variation2[i], 'price': unit_price3[i]}
                unit_price.append(unit_price2)
            category_name = category
            images = request.FILES.getlist("images")
            product = Products.objects.create(name=name, discription=discription, price=price, fav=fav,
                                              variation=variation1, category_name=category_name,
                                              unit_price=unit_price, unit=unit, feature_image=feature_image, type=type,
                                              unit_price_admin=unit_price1)
            for image in images:
                product_image = Product_image.objects.create(product=product, image=image)
            return JsonResponse({'Status': True, 'message': 'Product add sucessfull!', })
        except Exception as e:
            return JsonResponse({'Status': False, 'Exception': str(e), })
    return JsonResponse({'Status': False, 'message': 'Something went wrong!', })


def products_list(request):
    result = authorized(request)
    if result['status'] == True:
        if request.method == 'GET':
            products = Products.objects.all()
            product_serializer = ProductSerializer(products, many=True)
            return JsonResponse({'message': 'Banner listed successfully!', 'data': product_serializer.data}, safe=False)
    return JsonResponse({'message': 'Unauthorised User', })


@csrf_exempt
def product_edit(request):
    try:
        if request.method == 'POST':
            pk = request.POST.get('id')
            name = request.POST.get('name')
            category_name = request.POST.get('category_name')
            discription = request.POST.get('discription')
            price = request.POST.get('price')
            fav = request.POST.get('fav')
            unit = request.POST.get('unit')
            type = request.POST.get('type')
            variation1 = request.POST.get('variation')
            unit_price1 = request.POST.get('unit_price')
            feature_image = request.FILES["feature_image"]
            if ',' not in str(variation1) and ',' not in str(unit_price1):
                str(variation1) + ','
                str(unit_price1) + ','
            unit_price3 = unit_price1.split(',')
            variation2 = variation1.split(',')
            category = Category.objects.get(id=category_name)
            variation2 = variation1.split(',')
            unit_price2 = dict(zip(variation2, unit_price1))
            variation = str(variation2)
            unit_price = str(unit_price2)
            category_name = category
            images = request.FILES.getlist("images")
            product = Products.objects.filter(id=pk).update(name=name, discription=discription, price=price, fav=fav,
                                                            variation=variation1,
                                                            category_name=category_name,
                                                            unit_price=unit_price, unit=unit, type=type,
                                                            unit_price_admin=unit_price1)
            product_image = Products.objects.get(id=pk)
            product_image.feature_image = feature_image
            product_image.save()
            serializer = ProductSerializer(data=request.POST)
            for image in images:
                product_image = Product_image.objects.create_or_update(product=product, image=image)
            return JsonResponse({'Status': True, 'message': 'Product Edit sucessfull!', 'data': serializer.data, })
    except Exception as e:
        return JsonResponse({'Status': False, 'Exception': str(e), })


@csrf_exempt
def product_delete(request):
    if request.method == 'POST':
        pk = request.POST.get('id')
        product = Products.objects.filter(id=pk).delete()
        return JsonResponse({'message': 'Product deleted successfully!'})


@csrf_exempt
def add_to_cart(request):
    result = authorized(request)
    if result['status'] == True:
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            product1 = request.POST.get('product_id')
            price = request.POST.get('price')
            count = request.POST.get('count')
            variation = request.POST.get('variation')
            product = Products.objects.get(id=product1)
            user = User.objects.get(id=user_id)
            cart_serializer = CartSerializer(data=request.POST)
            cart_serializer.is_valid()
            try:
                cart = Cart.objects.filter(user=user, product=product).values('count', 'variation', 'price')
                cart1 = cart[0]
                variation1 = cart1['variation']
                price1 = cart1['price']
                count1 = cart1['count']
            except:
                cart = None
            if cart is not None and variation == variation1:
                count2 = int(count1) + int(count)
                price2 = int(price1) + int(price)
                cart = Cart.objects.filter(user=user, product=product, variation=variation).update(count=count2,
                                                                                                   price=price2)
            else:
                cart = Cart.objects.create(user=user, product=product, variation=variation, count=count, price=price)
                cart_serializer = CartSerializer(data=request.POST)
                cart_serializer.is_valid()
                #     pass
                # cart_serializer.save()
            return JsonResponse(
                {'message': 'Producst added to cart successfully!', 'data': cart_serializer.data,
                 })
        return JsonResponse(
            {'message': 'Something went wrong!',
             })
    return JsonResponse({"message": "Unauthorised User", })


@csrf_exempt
def edit_cart(request):
    result = authorized(request)
    if result['status'] == True:
        if request.method == "POST":
            user_id = request.POST.get('user_id')
            action = request.POST.get('action')
            count = request.POST.get('count')
            product_id = request.POST.get('product_id')
            variation = request.POST.get('variation')
            product = Products.objects.get(id=product_id)
            user = User.objects.get(id=user_id)
            price1 = Cart.objects.filter(user=user, product=product, variation=variation).values('price')
            price2 = price1[0]
            price = price2['price']
            real_price = int(price) / int(count)
            if action == '+':
                count1 = int(count) + 1
                price1 = int(price) + int(real_price)
            elif action == '-' and count == '1':
                Cart.objects.filter(user=user, product=product, variation=variation).delete()
                cart = cart = Cart.objects.filter(user=user).all()
                cart_serializer = CartSerializer(cart, many=True)
                return JsonResponse(
                    {'message': 'Cart editing successfully!', 'data': cart_serializer.data,
                     })
            else:
                count1 = int(count) - 1
                price1 = int(price) - int(real_price)
            count = count1
            cart = Cart.objects.filter(user=user, product=product, variation=variation).update(count=count,
                                                                                               price=price1)
            cart = Cart.objects.filter(user=user).all()
            cart_serializer = CartSerializer(cart, many=True)
            return JsonResponse(
                {'message': 'Cart editing successfully!', 'data': cart_serializer.data,
                 })
        return JsonResponse({'message': 'something went wrong!'})
    return JsonResponse({"message": "Unauthorised User", })


@csrf_exempt
def show_cart(request):
    result = authorized(request)
    if result['status'] == True:
        try:
            user_id = request.POST.get('user_id')
            user = User.objects.get(id=user_id)
            cart = Cart.objects.filter(user=user).all()
            cart_serializer = CartSerializer(cart, many=True)
            cart = Cart.objects.filter(user=user_id).values('price')
            price = 0
            for i in cart:
                price += int(i['price'])
            # print(cart_serializer.data)
            # exit()
            return JsonResponse(
                {'message': 'Cart Data!', 'data': cart_serializer.data, 'Gross price': price
                 })
        except:
            return JsonResponse(
                {'message': 'Cart Empty!',
                 })
    return JsonResponse(
        {'message': 'Unauthorized User',
         })


from datetime import datetime


@csrf_exempt
def add_coupon(request):
    if request.method == 'POST':
        coupon_name = request.POST.get('coupon_name')
        count = request.POST.get('count')
        discount = request.POST.get('discount')
        # print(request.POST.get('expire_date'))
        # exit()
        expire_date = datetime.datetime.strptime(request.POST.get('expire_date'), '%b %d %Y %I:%M%p')
        offers = Offers.objects.create(expire_date=expire_date, coupon_name=coupon_name, count=count, discount=discount)
        serializer = OfferSerializer(data=request.POST)
        serializer.is_valid()
        # serializer.save()
        return JsonResponse({
            'Message': 'coupon added success full',
        })
    return JsonResponse({'Message': 'Something went wrong',
                         })


@csrf_exempt
def delete_coupon(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        cop = Offers.objects.filter(id=id).delete()
        return JsonResponse({'message': 'Coupon deleted successfully!'})


from django.utils import timezone
import datetime


@csrf_exempt
def apply_coupon(request):
    result = authorized(request)
    if result['status'] == True:
        if request.method == 'POST':
            coupon_name = request.POST.get('coupon_name')
            user_id = request.POST.get('user_id')
            x = timezone.now()
            # print(x)
            # exit()
            try:
                cop = Offers.objects.filter(coupon_name=coupon_name).values('discount', 'count', 'expire_date')
                cart = Cart.objects.filter(user=user_id).values('price')
                price = 0
                cop1 = cop[0]
                for i in cart:
                    price += int(i['price'])
                discount = cop1['discount']
                count = cop1['count']
                expire_date = cop1['expire_date']
                print(price, discount, count, expire_date)
            except:
                cop = None
                price = 0
                discount = 0
                count = 0
                expire_date = ''
            if cop is not None and count > 0 and expire_date > x:
                discount1 = discount.split('%')
                price1 = int(price) * int(discount1[0]) / 100
                discount = int(price) - price1
                count -= 1
                offer = Offers.objects.filter(coupon_name=coupon_name).update(count=count)
                return JsonResponse(
                    {'message': 'Cart Data!', 'price': price1, 'discount': discount
                     })
        return JsonResponse(
            {'message': 'Something went Wrong',
             })
    return JsonResponse({"message": "Unauthorised User", })


@csrf_exempt
def edit_coupon(request):
    if request.method == "POST":
        id = request.POST.get('id')
        coupon_name = request.POST.get('coupon_name')
        count = request.POST.get('count')
        discount = request.POST.get('discount')
        # print(request.POST.get('expire_date'))
        # exit()
        expire_date = datetime.datetime.strptime(request.POST.get('expire_date'), '%b %d %Y %I:%M%p')
        offers = Offers.objects.filter(id=id).update(expire_date=expire_date, coupon_name=coupon_name, count=count,
                                                     discount=discount)
        serializer = OfferSerializer(data=request.POST)
        serializer.is_valid()
        # serializer.save()
        return JsonResponse({
            'Message': 'coupon added success full',
        })
    return JsonResponse({'Message': 'Something went wrong',
                         })


@csrf_exempt
def add_address(request):
    result = authorized(request)
    if result['status'] == True:
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            address = request.POST.get('address')
            locality = request.POST.get('locality')
            near_by = request.POST.get('near_by')
            pin = request.POST.get('pin')
            phone_no = request.POST.get('phone_no')
            user = User.objects.get(id=user_id)
            add = Address.objects.create(user=user, address=address, locality=locality, near_by=near_by, pin=pin,
                                         phone_no=phone_no)
            serializer = AddressSerializer(data=request.POST)
            serializer.is_valid()
            return JsonResponse(
                {'message': 'Address added sucessfull!',
                 })
        return JsonResponse({'message': 'Something went Wrong', })
    return JsonResponse({"message": "Unauthorised User", })


@csrf_exempt
def show_address(request):
    result = authorized(request)
    if result['status'] == True:
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            user = User.objects.get(id=user_id)
            address = Address.objects.filter(user=user).all()
            serializer = AddressSerializer(address, many=True)
            return JsonResponse(
                {'message': 'Cart Data!', 'data': serializer.data,
                 })
        return JsonResponse({'message': 'Something went wrong!!', })
    return JsonResponse({"message": "Unauthorised User", })


@csrf_exempt
def edit_address(request):
    result = authorized(request)
    if result['status'] == True:
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            id = request.POST.get('id')
            address = request.POST.get('address')
            locality = request.POST.get('locality')
            near_by = request.POST.get('near_by')
            pin = request.POST.get('pin')
            phone_no = request.POST.get('phone_no')
            user = User.objects.get(id=user_id)
            add = Address.objects.filter(user=user, id=id).update(address=address, locality=locality, near_by=near_by,
                                                                  pin=pin,
                                                                  phone_no=phone_no)
            serializer = AddressSerializer(data=request.POST)
            serializer.is_valid()
            return JsonResponse(
                {'message': 'Address Edited sucessfull!',
                 })
        return JsonResponse({'message': 'Something went Wrong', })
    return JsonResponse({"message": "Unauthorised User", })


@csrf_exempt
def delete_address(request):
    result = authorized(request)
    if result['status'] == True:
        if request.method == "POST":
            user_id = request.POST.get('user_id')
            id = request.POST.get('id')
            address = Address.objects.get(id=id, user=user_id).delete()
            return JsonResponse({'message': 'Address deleted successfully!'})
    return JsonResponse({"message": "Unauthorised User", })


@csrf_exempt
def checkout(request):
    result = authorized(request)
    if result['status'] == True:
        if request.method == "POST":
            user_id = request.POST.get('user_id')
            price = request.POST.get('price')
            transaction_id = request.POST.get('transaction_id')
            order_id = random.randint(111111, 999999)
            address_id = request.POST.get('address_id')
            products = Cart.objects.filter(user=user_id).values('product', 'count', 'variation')
            user = User.objects.get(id=user_id)
            address = Address.objects.filter(id=address_id)
            order_type = request.POST.get('order_type')
            for i in products:
                products = Products.objects.get(id=i['product'])
                order = Orders.objects.create(user=user, products=products, count=i['count'],
                                              transaction_id=transaction_id, price=price, address=address,
                                              order_id=order_id, variation=i['variation'], status='Confirmed',
                                              order_type=order_type, )
            Cart.objects.filter(user=user_id).delete()
            return JsonResponse({'message': 'order placed sucessfull!!', })
        return JsonResponse({'message': 'something went wrong!!', })
    return JsonResponse({"message": "unauthorised User", })


@csrf_exempt
def show_orders(request):
    result = authorized(request)
    if result['status'] == True:
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        order = Orders.objects.filter(user=user).all()
        order_serializer = OrdersSerializer(order, many=True)
        return JsonResponse(
            {'message': 'Orders Data!', 'data': order_serializer.data,
             })
    return JsonResponse({"message": "Unauthorised User", })


@csrf_exempt
def show_orders_admin(request):
    if request.method == 'POST':
        order = Orders.objects.all().order_by('-id')
        order_serializer = OrdersSerializer(order, many=True)
        return JsonResponse(
            {'Status': True, 'message': 'Orders Data!', 'data': order_serializer.data,
             })
    return JsonResponse(
        {'Status': False,
         })


@csrf_exempt
def edit_order(request):
    try:
        if request.method == 'POST':
            id = request.POST.get('id')
            status = request.POST.get('status')
            Orders.object.filter(id=id).update(status=status)
            return JsonResponse({'Status': True, 'message': 'order canceled!!'})
    except Exception as e:
        return JsonResponse({'Status': False, 'Exception': str(e)})


@csrf_exempt
def cancel_order(request):
    try:
        if request.method == 'POST':
            id = request.POST.get('id')
            status = request.POST.get('status')
            Orders.object.filter(id=id).update(status=status)
            return JsonResponse({'Status': True, 'message': 'order canceled!!'})
    except Exception as e:
        return JsonResponse({'Status': False, 'Exception': str(e)})


class Categoryapi(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class Productapi(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer


@csrf_exempt
def update_profile(request):
    result = authorized(request)
    if result['status'] == True:
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            image = request.FILES["image"]
            pk = request.POST.get('id')
            user_serializer = UserupdateSerializer(data=request.POST)
            # return JsonResponse(
            #     {'message': 'Data Updated successfully!', 'image': image,
            #      })
            if user_serializer.is_valid():
                category = User.objects.filter(id=pk).update(first_name=first_name, last_name=last_name, email=email,
                                                             phone=phone)
                users = User.objects.get(id=pk)
                users.image = image
                users.save()
                # user = UserupdateSerializer(users)
                return JsonResponse(
                    {'message': 'Data Updated successfully!', 'data': user_serializer.data,
                     })
            else:
                return JsonResponse(
                    {'message': 'unexpected error'
                     })
    return JsonResponse({"message": "Unauthorised User", })


@csrf_exempt
def show_user(request):
    if request.method == "POST":
        id = request.POST.get('id')
        user = User.objects.filter(id=id).values("first_name", "last_name", "email", "phone", "image")[0]
        return JsonResponse(
            {'message': 'User data!', 'data': user,
             })


@api_view(['POST'])
@csrf_exempt
def admin_login(request, format=json):
    parser_classes = [JSONParser]
    tok = MyTokenObtainPairSerializer()
    content = request.data
    email = content['email']
    # print(email)
    # exit()
    if request.method == 'POST':
        email = content['email']
        password = content['password']
        try:
            password1 = User.objects.filter(email=email).values('password')[0]
            users = User.objects.get(email=email)
        except:
            password1 = {'password': ''}
        if check_password(password, password1['password']) == True:
            token = tok.get_token(users)
            stoken = str(token)
            user_token = User.objects.filter(email=email).update(token=stoken)
            users_serializer = AdminSerializer(users)
            return JsonResponse(
                {'Status': True, 'Message': 'User logged in successfully!', 'Data': users_serializer.data,
                 'token': stoken,
                 })
        else:
            return JsonResponse(
                {'Status': False, 'Message': 'Wrong Credentials!',
                 })


@api_view(['POST'])
@csrf_exempt
def check_token(request, format=json):
    parser_classes = [JSONParser]
    content = request.data
    if request.method == 'POST':
        id = content['id']
        token = content['token']
        stoken = User.objects.filter(id=id).values('token')[0]
        if token == stoken:
            return JsonResponse({'Status': True, 'Message': 'sucessfully login!!',
                                 })
    return JsonResponse(
        {'Status': False, 'Message': 'Wrong Credentials!',
         })


@csrf_exempt
def auth_otp(request):
    result = authorized(request)
    if result['status'] == True:
        tok = MyTokenObtainPairSerializer()  # object to get user token
        if request.method == 'POST':
            id = request.POST.get('id')
            otp = request.POST.get('otp')
            users = User.objects.get(id=id)
            otp_stored = User.objects.filter(id=id).values('otp')[0]
            print(type(otp))
            if otp == str(otp_stored['otp']):
                print("yesssss")
                users_serializer = UserSerializer(users)
                token = tok.get_token(users)
                stoken = str(token)
                return JsonResponse(
                    {'Status': True, 'data': users_serializer.data, 'token': stoken,
                     'otp': otp})
            else:
                users_serializer = UserSerializer(users)
                return JsonResponse(
                    {'Status': False, 'data': users_serializer.data,
                     })
    return JsonResponse({"message": "Unauthorised User", })


# extra code for login and register
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


from rest_framework import generics


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


import stripe

stripe.api_key = 'sk_test_51JbfHOSEqSPPnpJQuwEGeMRmW3L4h0iXiXO5uJnVNz60w87Eq1ghXzHO5h4zrCJPuYnik9FclvPpKVIOpSMgg1by0020O8cjbu'


@csrf_exempt
def test_payment(request):
    test_payment_intent = stripe.PaymentIntent.create(
        amount=1000, currency='pln',
        payment_method_types=['card'],
        receipt_email='test@example.com')
    return JsonResponse(status=status.HTTP_200_OK, data=test_payment_intent)


@csrf_exempt
def save_stripe_info(request):
    data = request.POST
    email = data['email']
    amount = data['amount']
    payment_method_id = data['payment_method_id']
    source = data['token']
    extra_msg = ''  # add new variable to response message
    # checking if customer with provided email already exists
    customer_data = stripe.Customer.list(email=email).data

    # if the array is empty it means the email has not been used yet
    if len(customer_data) == 0:
        # creating customer
        customer = stripe.Customer.create(
            email=email, payment_method=payment_method_id)
        charge = stripe.Charge.create(
            amount=amount,
            currency="usd",
            description="My First Test Charge (created for API docs)",
            source=source,  # obtained with Stripe.js
            idempotency_key='j41Tr6PLICmzJtG2'
        )
    else:
        customer = customer_data[0]
        extra_msg = "Customer already existed."
    charge = stripe.Charge.create(
        amount=amount,
        currency="usd",
        description="My First Test Charge (created for API docs)",
        source=source,  # obtained with Stripe.js
        idempotency_key='j41Tr6PLICmzJtG2'
    )
    return JsonResponse(status=status.HTTP_200_OK,
                        data={'message': 'Success', 'data': {
                            'customer_id': customer.id, 'extra_msg': extra_msg}
                              })


# dine_in ---- API ----

@csrf_exempt
def add_dinein(request):
    try:
        if request.method == 'POST':
            total_tables = request.POST.get('total_tables')
            date = datetime.datetime.strptime(request.POST.get('date'), '%b %d %Y %I:%M%p')
            status = request.POST.get('total_tables')
            Dine_in.objects.create(total_tables=total_tables, date=date, status=status)
            return JsonResponse({"Status": True, })
    except Exception as e:
        return JsonResponse({'Status': False, 'Exception': str(e), })


@csrf_exempt
def edit_dinein(request):
    try:
        if request.method == 'POST':
            id = request.POST.get('id')
            total_tables = request.POST.get('total_tables')
            date = datetime.datetime.strptime(request.POST.get('date'), '%b %d %Y %I:%M%p')
            status = request.POST.get('total_tables')
            Dine_in.objects.filter(id=id).update(total_tables=total_tables, date=date, status=status)
            return JsonResponse({"Status": True, })
    except Exception as e:
        return JsonResponse({'Status': False, 'Exception': str(e), })


@csrf_exempt
def show_dinein(request):
    if request.method == 'POST':
        dien = Dine_in.objects.all().order_by('-id')
        dien_serializer = DieninSerializer(dien, many=True)
        return JsonResponse(
            {'Status': True, 'message': 'Banner listed successfully!', 'data': dien_serializer.data}, safe=False)
    return JsonResponse({'Status': False, 'message': 'Something went wrong!', })


@csrf_exempt
def delete_dinein(request):
    if request.method == "POST":
        id = request.POST.get('id')
        try:
            dien = Dine_in.objects.get(id=id)
            dien.delete()
            return JsonResponse({'Status': True, 'message': 'Category deleted successfully!'})
        except:
            return JsonResponse({'Status': False, 'message': 'Id not found!'})


@csrf_exempt
def add_booking(request):
    result = authorized(request)
    if result['status'] == True:
        try:
            if request.method == "POST":
                user_id = request.POST.get('user_id')
                date = request.POST.get('date')
                dien_id = request.POST.get('dien_id')
                user = User.Objects.get(id=user_id)
                total_table = Dine_in.objects.filter(id=dien_id).values('total_tables')
                total_table1 = total_table[0]
                if total_table1['total_tables'] > 0:
                    Booking.objects.create(user=user, date=datetime.datetime.strptime(date, '%b %d %Y %I:%M%p'))
                    total_table = int(total_table1['total_tables']) - 1
                    Dine_in.objects.filter(id=dien_id).update(total_tables=total_table)
                    return JsonResponse({"Status": True, "message": "Booked"})
        except Exception as e:
            return JsonResponse({"Status": False, "message": "Something went wrong!!"})
    return JsonResponse({"message": "Unauthorised User"})


@csrf_exempt
def show_booking(request):
    result = authorized(request)
    if result['status'] == True:
        if request.method == "POST":
            user_id = request.POST.get('user_id')
            user = User.objects.get(id=user_id)
            address = Booking.objects.filter(user=user).all().order_by('-id')
            serializer = BookingSerializer(address, many=True)
            return JsonResponse(
                {'message': 'Users Address!', 'data': serializer.data,
                 })
        return JsonResponse({'message': 'Something went wrong!!', })
    return JsonResponse({"message": "Unauthorised User"})


@csrf_exempt
def show_booking_admin(request):
    if request.method == "POST":
        address = Booking.objects.all().order_by('-id')
        serializer = BookingSerializer(address, many=True)
        return JsonResponse(
            {"Status": True, 'message': 'Users Address!', 'data': serializer.data,
             })
    return JsonResponse({"Status": False, 'message': 'Something went wrong!!', })


@csrf_exempt
def cancel_booking(request):
    result = authorized(request)
    if result['status'] == True:
        if request.method == "POST":
            user_id = request.POST.get('user_id')
            id = request.POST.get('booking_id')
            user = User.objects.get(id=user_id)
            booking = Booking.objects.filter(id=id, user=user).update(status='canceled')
            return JsonResponse({"Status": True, "message": 'Booking canceled'})
        return JsonResponse({"Status": False, })
    return JsonResponse({"message": "Unauthorised User"})


@csrf_exempt
def add_review(request):
    result = authorized(request)
    if result['status'] == True:
        if request.method == "POST":
            user_id = User.objects.get(id=request.POST.get('user_id'))
            product_id = Products.objects.get(id=request.POST.get('product_id'))
            review = request.POST.get('review')
            rating = request.POST.get('rating')
            Review.objects.create(user=user_id, product=product_id, review=review, rating=rating)
            return JsonResponse({"Status": True, "message": "Sucess"})
        return JsonResponse({"Status": False, 'message': "Something went wrong!!"})
    return JsonResponse({"message": "Unauthorised User"})


@csrf_exempt
def edit_review(request):
    result = authorized(request)
    if result['status'] == True:
        if request.method == "POST":
            id = request.POST.get('id')
            user_id = User.objects.get(id=request.POST.get('user_id'))
            product_id = Products.objects.get(id=request.POST.get('product_id'))
            review = request.POST.get('review')
            rating = request.POST.get('rating')
            Review.objects.filter(id=id).update(user=user_id, product=product_id, review=review, rating=rating)
            return JsonResponse({"Status": True, "message": "Sucess"})
        return JsonResponse({"Status": False, 'message': "Something went wrong!!"})
    return JsonResponse({"message": "Unauthorised User"})


@csrf_exempt
def show_review(request):
    if request.method == 'POST':
        review = Review.objects.all().order_by('-id')
        review_serializer = DieninSerializer(review, many=True)
        return JsonResponse(
            {'Status': True, 'message': 'Banner listed successfully!', 'data': review_serializer.data}, safe=False)
    return JsonResponse({'Status': False, 'message': 'Something went wrong!', })


@csrf_exempt
def delete_review(request):
    if request.method == "POST":
        id = request.POST.get('id')
        review = Review.objects.get(id=id).delete()
        return JsonResponse({'Status': True, 'message': 'Address deleted successfully!'})
    return JsonResponse({'Status': False, "message": "Unauthorised User", })


def create_bitly(request):
    query_params = {'phone': '8743951646'}
    endpoint = 'http://amantiwarii4.pythonanywhere.com/banner/banner_list_client/'
    # try:
    files = {'media': open('Downloads/aman.jpg', 'rb')}
    response = requests.post(endpoint,
                             data={'email': 'i4@gmail.com', 'id': '43', 'first_name': 'aman', 'last_name': 'tiwari',
                                   'phone': '900989', }, files=files)
    # response = requests.get(endpoint)
    # bitly_url = json.loads(response.content.decode('utf-8'))
    data = response.json()
    print(data)
    exit()
    data1 = data['data']
    for i in data1:
        j = i['image']
        k = 'http://amantiwarii4.pythonanywhere.com' + j
        i['image'] = k
        i['url'] = i['image']

    print(data1)
    exit()
    # short_url = bitly_url['data']['url']
    # except:
    short_url = ''
    return short_url
