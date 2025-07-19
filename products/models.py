from django.db import models
from django.contrib.auth.models import User


class Catagory(models.Model):
    name = models.CharField(max_length=120, null=True)

    def __str__(self):
        return self.name

class Techs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Catagory, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    camera = models.CharField(default='12MP', max_length=8)
    batareya = models.CharField(max_length=10, default='4500mAh')
    harakteri = models.TextField()
    deck = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    image = models.ImageField(upload_to='books-images/', blank=True, null=True, default='default/Logitech2.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updates_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', ]


    def __str__(self):
        return self.title
# Create your models here.
