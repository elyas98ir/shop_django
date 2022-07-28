from django.urls import path
from . import views


app_name = 'panel'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('payments/', views.PaymentListView.as_view(), name='payments'),
]
