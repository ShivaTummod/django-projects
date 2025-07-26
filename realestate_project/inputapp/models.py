from django.db import models

# Create your models here.
class InputTable(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact = models.IntegerField()
    flat_price = models.IntegerField()
    square_feet = models.IntegerField()
    
    def __str__(self):
        return self.name