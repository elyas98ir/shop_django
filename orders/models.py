from django.db import models
from accounts.models import User
from products.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    recipient_name = models.CharField(max_length=100)
    recipient_phone_number = models.CharField(max_length=11)
    recipient_address = models.CharField(max_length=250)
    coupon_code = models.CharField(max_length=20, default=None, null=True, blank=True)
    coupon_discount = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, )

    class Meta:
        ordering = ('paid', '-id',)

    def __str__(self):
        return f'order - {self.user}'

    def get_total_cost(self, without_discount):
        total = sum(item.get_item_cost() for item in self.items.all())
        total_with_discount = total

        if self.coupon_code and self.coupon_discount:
            discount_price = (self.coupon_discount / 100) * total
            total_with_discount = int(total - discount_price)

        if without_discount:
            return total
        return total_with_discount


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1, )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f'orderitem {self.order}'

    def get_item_cost(self):
        return self.price * self.quantity


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='user')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='order')
    amount = models.PositiveIntegerField()
    authority = models.CharField(max_length=250)
    status = models.BooleanField(default=False)
    tracking_code = models.CharField(max_length=100, default=None, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('status', '-id')

    def __str__(self):
        return f'{self.tracking_code} - {self.status}'


class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount = models.PositiveSmallIntegerField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f'{self.code} - {self.discount}'
