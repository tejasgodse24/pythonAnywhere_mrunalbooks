from django.db import models
from base.models import BaseModel

# Create your models here.

class Courier(BaseModel):
    name = models.CharField(max_length=50)
    courier_charge = models.IntegerField()
    is_active = models.BooleanField(default = True)

    def __str__(self):
        return self.name
