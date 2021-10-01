from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Banner, Category, Products, Product_image, Cart, Orders, Offers, Address, Dine_in, Booking, Review


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token


# Register_serializer

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class ProductimageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_image
        # fields = ()
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        # fields = ()
        fields = '__all__'


class CategoryadminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # fields = ('id', 'username', 'email', 'password', 'phone', 'first_name', 'last_name', 'user_role', 'about', 'user_image')
        fields = '__all__'


class BannerclientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('image',)
        # fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    images = ProductimageSerializer(read_only=True, many=True)
    product_review = ReviewSerializer(read_only=True, many=True)

    class Meta:
        model = Products
        # fields = ('name','category_name','discription','price','fav','unit','unit_price','variation')
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(read_only=True, many=True)

    class Meta:
        model = Category
        # fields = ('id', 'username', 'email', 'password', 'phone', 'first_name', 'last_name', 'user_role', 'about', 'user_image')
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ('id','username','email','password','phone','first_name','last_name')
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'


class UserupdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'phone', 'first_name', 'last_name', 'image')
        # fields = '__all__'


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'last_login', 'email', 'username', 'is_superuser')
        # fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offers
        # fields = ('id', 'last_login', 'email', 'username', 'is_superuser')
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        # fields = ('id', 'last_login', 'email', 'username', 'is_superuser')
        fields = '__all__'


class OrdersSerializer(serializers.ModelSerializer):
    products = ProductSerializer(read_only=True)
    users = UserSerializer(read_only=True)
    addresses = AddressSerializer(read_only=True)

    class Meta:
        model = Orders
        fields = '__all__'


class DieninSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dine_in
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
