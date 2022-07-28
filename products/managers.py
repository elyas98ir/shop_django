from django.db import models


class CategoryManager(models.Manager):
    def main_categories(self):
        return self.filter(parent__isnull=True)


class ProductManager(models.Manager):
    def availables(self):
        return self.filter(available=True, stock_quantity__gte=1)
