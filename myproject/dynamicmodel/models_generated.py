from django.db import models

class book(models.Model):
    name = models.TextField(default='')
