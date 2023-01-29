from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
class resizer(models.Model):
    resized_image = CloudinaryField('image')
    