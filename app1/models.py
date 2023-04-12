from django.db import models

class Image(models.Model):
    image_name = models.CharField(max_length=100)
    objects_detected = models.CharField(max_length=500)
    timestamp = models.DateTimeField()
    image = models.ImageField(upload_to='media/objs/')

    def __str__(self) -> str:
        return self.image_name
    
    class Meta:
        db_table = "ImageList"

