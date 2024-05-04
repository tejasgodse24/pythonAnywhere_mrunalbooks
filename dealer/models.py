from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel


# Create your models here.

class Dealer(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dealer', null=True, blank=True)
    fname = models.CharField(max_length=20, null=True, blank=True)
    lname = models.CharField(max_length=20, null=True, blank=True)
    phone =  models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.fname + " " + self.lname


class Dealer_Address(BaseModel):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name='dealer_addressess')
    name = models.CharField(max_length = 50)
    shop_name  = models.CharField(max_length = 100, null=True, blank=True)
    pincode = models.CharField(max_length = 6)
    area = models.CharField(max_length = 100)
    adss1 =  models.CharField(max_length = 1000, null=True, blank=True) #locality/street name/apartment
    adss2 =  models.CharField(max_length = 1000, null=True, blank=True) #shopNo. / Wing NO.
    adss3 =  models.CharField(max_length = 1000, null=True, blank=True) #landmark
    city = models.CharField(max_length = 100)
    state =  models.CharField(max_length = 100)

    def __str__(self):
        if self.adss3:
            return self.shop_name + ", " + self.adss2 + ", " + self.adss3 + ", " + self.area + ", " + self.city + ", " + self.state + ", " + self.pincode
        return self.shop_name + ", " + self.adss2 + ", " + self.adss1 + ", " + self.area + ", " + self.city + ", " + self.state + ", " + self.pincode


