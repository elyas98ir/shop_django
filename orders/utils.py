from .cart import Cart


def get_cart_infos(request):
    coupon_code = request.session.get('coupon_code')
    coupon_discount = request.session.get('coupon_discount')

    cart = Cart(request)
    total_price = cart.get_total_cost()
    total_price = total_price.replace(',', '')
    total_price = int(total_price)

    if coupon_code and coupon_discount:
        discount_price = int((coupon_discount / 100) * total_price)
    else:
        discount_price = 0
    total_cost = int(total_price - discount_price)

    return coupon_code, coupon_discount, total_price, discount_price, total_cost
