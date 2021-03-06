from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=400)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    ipfspath = models.CharField(max_length=300)
    metadatapath = models.CharField(max_length=300)
    contractaddress = models.CharField(max_length=300)
    openseaurl = models.CharField(max_length=300)
    nftimagefile = models.FileField(upload_to = "uploads/")
    is_approved = models.BooleanField(default=False)
    upi = models.CharField(max_length=400)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title