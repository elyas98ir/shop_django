from django.urls import path
from . import views


app_name = 'products'

urlpatterns = [
    path('products/', views.ProductList.as_view(), name='products_list'),
    path('products/<slug:slug>/', views.ProductDetail.as_view(), name='products_detail'),
    path('category/<slug:slug>/', views.CategoryProductList.as_view(), name='category_products'),
]
