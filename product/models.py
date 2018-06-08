from django.db import models

class Featured(models.Model):
    name = models.CharField(max_length=200, unique=True)
    fixed_price = models.FloatField(null=True)
    discounted_price = models.FloatField(null=True)
    pic_name = models.CharField(max_length=300)
    size = models.CharField(max_length=30)
    category = models.CharField(max_length=30)

    class Meta:
        ordering = ["-category"]
