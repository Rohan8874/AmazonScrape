from django.db import models

class ProductURL(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=50)
    hero_image_url = models.URLField()

    def __str__(self):
        return self.title