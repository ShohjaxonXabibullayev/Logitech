from django.db import models
from django.contrib.auth.models import User


class Catagory(models.Model):
    name = models.CharField(max_length=120, null=True)

    class Meta:
        db_table = 'category'

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
        db_table = 'techs'
        ordering = ['-created_at', ]


    def __str__(self):
        return self.title

class Comment(models.Model):
    tech = models.ForeignKey(Techs, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', ]
        db_table = 'comments'

    def __str__(self):
        return self.tech.title

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    email = models.EmailField()
    info = models.CharField(max_length=120, blank=True, null=True)
    text = models.TimeField(default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', ]
        db_table = 'contacts'

    def __str__(self):
        return self.name

class Saved(models.Model):
    news = models.ForeignKey(Techs, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'saved'
# Create your models here.
