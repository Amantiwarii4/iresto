from django.urls import path, include
from banner.views import MyObtainTokenPairView, RegisterView, getPhoneNumberRegistered_TimeBased, \
    getPhoneNumberRegistered_TimeBased
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf.urls import include, url
from . import views

urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    # path("<phone>/", getPhoneNumberRegistered.as_view(), name="OTP Gen"),
    path('add_banner/', views.add_banner, name="Add Banner"),
    path('add_category/', views.add_category, name="Add Category"),
    path('category_list/', views.category_list, name="Show All Category"),
    path('user_login/', views.user_login, name="login"),
    # path('category_edit/<int:pk>/', views.category_edit, name="Edit Category"),
    url(r'^category_edit/(?P<pk>\d+)/', views.category_edit, name='Edit Category'),
    # path("time_based/<phone>/", getPhoneNumberRegistered_TimeBased.as_view(), name="OTP Gen Time Based"),
]
