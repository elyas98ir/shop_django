from django.db import models
from .managers import CategoryManager, ProductManager


class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CategoryManager()

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='products')
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    image = models.ImageField(upload_to='products/images/')
    description = models.TextField()
    price = models.PositiveIntegerField()
    stock_quantity = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ProductManager()

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.name

    def seprated_price(self):
        return f'{self.price:,}'

    def categories(self):
        return ', '.join([category.name for category in self.category.all()])
    categories.short_description = 'دسته‌بندی‌ها'
