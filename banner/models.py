from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, blank=True)
    discription = models.CharField(max_length=1000, blank=True)
    author_id = models.CharField(max_length=50, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Banner(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    category_name = models.ForeignKey(Category, related_name='products', null=False, on_delete=models.CASCADE)
    type = models.BooleanField(default=False)
    discription = models.CharField(max_length=1000, blank=True)
    price = models.IntegerField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fav = models.BooleanField(default=False)
    variation = models.CharField(max_length=1000, blank=True)
    unit = models.CharField(max_length=20, blank=True)
    unit_price = models.CharField(max_length=1000, blank=True)
    unit_price_admin = models.TextField(default='')
    feature_image = models.ImageField(null=True, blank=True, upload_to='images/')


class Product_image(models.Model):
    product = models.ForeignKey(Products, related_name='images', null=False, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='images/')


class Cart(models.Model):
    user = models.ForeignKey(User, related_name='user', null=False, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, related_name='product', null=False, on_delete=models.CASCADE)
    variation = models.CharField(max_length=1000, blank=True)
    price = models.IntegerField(blank=False)
    count = models.IntegerField(blank=False, default=1)


class Offers(models.Model):
    id = models.AutoField(primary_key=True)
    coupon_name = models.CharField(max_length=100, blank=True)
    expire_date = models.DateTimeField()
    count = models.IntegerField(blank=False)
    discount = models.CharField(max_length=100, blank=True)


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='user_info', null=False, on_delete=models.CASCADE)
    address = models.CharField(max_length=500, blank=False)
    locality = models.CharField(max_length=500, blank=False)
    near_by = models.CharField(max_length=500, blank=False)
    pin = models.CharField(max_length=20, blank=False)
    phone_no = models.CharField(max_length=20, blank=False)


class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='users', null=False, on_delete=models.CASCADE)
    products = models.ForeignKey(Products, related_name='products', null=False, on_delete=models.CASCADE)
    variation = models.CharField(max_length=1000, blank=True)
    price = models.IntegerField(blank=False)
    address = models.ForeignKey(Address, related_name='addresses', default=1, null=False, on_delete=models.CASCADE)
    count = models.IntegerField(blank=False, default=1)
    order_id = models.CharField(max_length=1000, blank=True)
    transaction_id = models.CharField(max_length=1000, blank=True)
    status = models.CharField(max_length=200, blank=True, default='Order Confirmed')
    order_type = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Dine_in(models.Model):
    id = models.AutoField(primary_key=True)
    total_tables = models.IntegerField(blank=False)
    date = models.DateTimeField()
    status = models.CharField(max_length=200, blank=True)


class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='user_name', null=False, on_delete=models.CASCADE)
    status = models.CharField(max_length=200, blank=True, default='Booked')
    date = models.DateTimeField()


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='user_review', null=False, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, related_name='product_review', null=False, on_delete=models.CASCADE)
    review = models.TextField(blank=True, )
    rating = models.IntegerField()
    status = models.CharField(max_length=200, blank=True)
