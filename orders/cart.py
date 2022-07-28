from products.models import Product
from django.shortcuts import get_object_or_404

CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['total_price'] = int(item['price']) * int(item['quantity'])
            item_price = item['price']
            total_price = item['total_price']
            item['price'] = f'{item_price:,}'
            item['total_price'] = f'{total_price:,}'
            yield item

    def __len__(self):
        return len(self.cart)

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'price': product.price, 'quantity': 0}
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()

    def update(self, products_quantity):
        quantity_list = products_quantity.split(',')
        quantity_list.pop()
        quantity_list.reverse()
        print('-' * 100)
        print(quantity_list)
        print('-' * 100)
        if len(quantity_list) == len(self.cart):
            for item in self.cart.values():
                item['quantity'] = int(quantity_list.pop())
            self.save()

    def get_quantity(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            return int(self.cart[product_id]['quantity'])
        return None

    def get_total_cost(self):
        total = sum((int(item['price']) * int(item['quantity'])) for item in self.cart.values())
        return f'{total:,}'

    def check_quantiry(self):
        messages = []
        for product_id, item in self.cart.items():
            product = get_object_or_404(Product, id=product_id)
            quantity = item['quantity']
            if product.stock_quantity < quantity:
                messages.append(f'فقط {product.stock_quantity} عدد از {product.name} در انبار موجود است')
        return messages

    def save(self):
        self.session.modified = True
