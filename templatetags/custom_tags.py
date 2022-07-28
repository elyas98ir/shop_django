from django import template
from products.models import Category
from orders.cart import Cart


register = template.Library()


@register.inclusion_tag('products/partials/product_card.html')
def product_card(product):
    return {
        'product': product
    }


@register.inclusion_tag('products/partials/category_navbar.html')
def navbar_category():
    return {
        'category': Category.objects.all()
    }
