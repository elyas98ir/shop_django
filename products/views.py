from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.db.models import Q
from .models import Category, Product
from django.views.generic import ListView, DetailView
from orders.forms import CartAddFormForm
from orders.cart import Cart


class ProductList(ListView):
    paginate_by = 9

    def get_queryset(self):
        orderby = self.request.GET.get('orderby', None)
        search = self.request.GET.get('q', None)

        if search:
            return Product.objects.availables().filter(Q(name__contains=search) | Q(description__contains=search))

        if orderby == 'id_asc':
            return Product.objects.availables().order_by('id')
        elif orderby == 'id_desc':
            return Product.objects.availables().order_by('-id')
        elif orderby == 'price_asc':
            return Product.objects.availables().order_by('price')
        elif orderby == 'price_desc':
            return Product.objects.availables().order_by('-price')
        else:
            return Product.objects.availables()
        return super().get_queryset()


class ProductDetail(DetailView):
    queryset = Product.objects.availables()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CartAddFormForm
        cart = Cart(self.request)
        context["cart_quantity"] = cart.get_quantity(self.get_object())
        return context


class CategoryProductList(ListView):
    paginate_by = 9
    template_name = 'products/category_product_list.html'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug=slug)
        return category.products.availables()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = category
        return context
