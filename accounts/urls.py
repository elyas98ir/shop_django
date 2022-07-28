from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # path('', views.HomeView.as_view(), name='home'),
    path('auth/', views.UserOTPSendView.as_view(), name='otp_send'),
    path('auth/otp/', views.UserOTPVerifyView.as_view(), name='otp_verify'),
]