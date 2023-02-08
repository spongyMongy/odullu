from django.db import models

# Create your models here.


class GiftModelAutoScraping(models.Model):
    picture = models.ImageField()#(upload_to='media/')
    link = models.URLField()
    time = models.DateTimeField(auto_now_add=True)
    gift_name = models.CharField(max_length=100)

    def __str__(self):
        return self.gift_name



class GiftModelUserEntry(models.Model):
    picture = models.ImageField(upload_to='media/', null=True, blank=True)
    link = models.URLField()
    time = models.DateTimeField(auto_now_add=True)
    gift_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, null=True, blank=True)
    thumbnail_link = models.URLField()

    def __str__(self):
        return self.gift_name