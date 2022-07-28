from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .cart import Cart
from products.models import Product
from .forms import CartAddFormForm, CouponCodeForm, OrderCheckoutForm
from .models import Order, OrderItem, Payment, Coupon
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import get_cart_infos
from . import pay
from django.http import HttpResponse


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        form = CouponCodeForm()
        coupon_code, coupon_discount, total_price, discount_price, total_cost = get_cart_infos(request)
        return render(request, 'orders/cart.html', {
            'cart': cart, 'form': form,
            'coupon_code': coupon_code,
            'coupon_discount': coupon_discount,
            'total_price': f'{total_price:,}',
            'discount_price': f'{discount_price:,}',
            'total_cost': f'{total_cost:,}',
        })


class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddFormForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('orders:cart')


class CartRemoveView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('orders:cart')


class CartUpdateView(View):
    def post(self, request):
        cart = Cart(request)
        cart.update(request.POST.get('quantity'))
        return redirect('orders:cart')


class CouponCodeView(View):
    def post(self, request):
        form = CouponCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            now = timezone.now()
            try:
                coupon = Coupon.objects.get(code__exact=code, valid_to__gte=now, active=True)
                request.session['coupon_code'] = coupon.code
                request.session['coupon_discount'] = coupon.discount
            except Coupon.DoesNotExist:
                messages.error(request, 'کد تخفیف وارد شده معتبر نمی‌باشد', 'danger')
            return redirect('orders:cart')
        return redirect('orders:cart')


class CouponCodeDeleteView(View):
    def get(self, request):
        del request.session['coupon_code']
        del request.session['coupon_discount']
        return redirect('orders:cart')


class CheckoutView(LoginRequiredMixin, View):
    form_class = OrderCheckoutForm

    def get(self, request):
        cart = Cart(request)
        if not cart:
            return redirect('orders:cart')

        form = self.form_class
        coupon_code, coupon_discount, total_price, discount_price, total_cost = get_cart_infos(request)

        quantity_messages = cart.check_quantiry()

        if len(quantity_messages) == 0:
            return render(request, 'orders/checkout.html', {
                'cart': cart, 'form': form,
                'coupon_code': coupon_code,
                'coupon_discount': coupon_discount,
                'total_price': f'{total_price:,}',
                'discount_price': f'{discount_price:,}',
                'total_cost': f'{total_cost:,}',
            })
        else:
            for msg in quantity_messages:
                messages.error(request, msg, 'danger')
            form = CouponCodeForm(request.POST)
            return render(request, 'orders/cart.html', {
                'cart': cart, 'form': form,
                'coupon_code': coupon_code,
                'coupon_discount': coupon_discount,
                'total_price': f'{total_price:,}',
                'discount_price': f'{discount_price:,}',
                'total_cost': f'{total_cost:,}',
            })

    def post(self, request):
        cart = Cart(request)
        if not cart:
            return redirect('orders:cart')

        form = self.form_class(request.POST)
        coupon_code, coupon_discount, total_price, discount_price, total_cost = get_cart_infos(request)

        if form.is_valid():
            cd = form.cleaned_data
            order = Order.objects.create(
                user=request.user,
                recipient_name=cd['recipient_name'],
                recipient_phone_number=cd['recipient_phone_number'],
                recipient_address=cd['recipient_address'],
                coupon_code=coupon_code,
                coupon_discount=coupon_discount
            )
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'].replace(',', ''),
                    quantity=item['quantity']
                )
            return pay.send(request, order)

        return render(request, 'orders/checkout.html', {
            'cart': cart, 'form': form,
            'coupon_code': coupon_code,
            'coupon_discount': coupon_discount,
            'total_price': f'{total_price:,}',
            'discount_price': f'{discount_price:,}',
            'total_cost': f'{total_cost:,}',
        })


class OrderPayVerify(View):
    def get(self, request):
        return pay.verify(request)
