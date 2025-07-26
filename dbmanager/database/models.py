from django.db import models

# Create your models here.


class AuditLog(models.Model):
    table_name = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.table_name} - {self.action}"