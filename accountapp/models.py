from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


# Create your models here.

class Savedpasswords(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    domain = models.CharField(max_length=200, blank=True)
    email  = models.CharField(max_length=200,blank=True)
    username = models.CharField(max_length=200,blank=True)
    password = models.CharField(max_length=200,blank=True)
    of_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=30, editable=True, blank=True)

    def __str__(self):
        return self.domain
    
    def get_absolute_url(self):
        return reverse("savedpasswords_detail", kwargs={"pk": self.pk})
        # return reverse("savedpasswords_detail", args = [self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Savedpasswords, self).save(*args,**kwargs)

    



    

    