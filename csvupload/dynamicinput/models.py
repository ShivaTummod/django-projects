from django.db import models

class UserDatas(models.Model):
    field_name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=50)
    field_value = models.TextField()

    def __str__(self):
        return f"{self.field_name} ({self.field_type}) = {self.field_value}"
