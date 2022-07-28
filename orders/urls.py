from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>/', views.CartAddView.as_view(), name='cart_add'),
    path('cart/remove/<int:product_id>/', views.CartRemoveView.as_view(), name='cart_remove'),
    path('cart/update/', views.CartUpdateView.as_view(), name='cart_update'),
    path('cart/coupon/', views.CouponCodeView.as_view(), name='cart_coupon'),
    path('cart/coupon/delete/', views.CouponCodeDeleteView.as_view(), name='cart_coupon_delete'),
    path('cart/checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('orders/pay/verify/', views.OrderPayVerify.as_view(), name='pay_verify'),
]
