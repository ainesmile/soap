from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = (
        ('B', 'Best'),
        ('F', 'Featured'),
        ('N', 'Normal')
    )
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=200, unique=True)
    fixed_price = models.FloatField(null=True)
    discounted_price = models.FloatField(null=True)
    pic_name = models.CharField(max_length=300)
    size = models.CharField(max_length=30)
    subcategory = models.CharField(max_length=30)

    class Meta:
        ordering = ['category', '-subcategory']
