
from typing import Any
from django.forms import ModelForm, TextInput
from django import forms
from accounts.models import Address
from products.models import Product
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User



class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def clean_title(self):
        title = self.cleaned_data['title']
        return title



class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = "__all__"
        exclude = ["is_default", "user"]

        labels = {
            "name": _("Name"),
            "adss1": _("Locality/ Street Name/ Apartment"),
            "adss2": _("Wing/ Floor/ Flat/ House No."),
            "adss3": _("Landmark(optional)"),
        }
        widgets = {
            "name" : TextInput(attrs={"class" : "form-control"}),
            "pincode" : TextInput(attrs={"class" : "form-control"}),
            "area" : TextInput(attrs={"class" : "form-control"}),
            "adss1" : TextInput(attrs={"class" : "form-control"}),
            "adss2" : TextInput(attrs={"class" : "form-control"}),
            "adss3" : TextInput(attrs={"class" : "form-control"}),
            "city" : TextInput(attrs={"class" : "form-control"}),
            "state" : TextInput(attrs={"class" : "form-control"}),
            "phone" : TextInput(attrs={"class" : "form-control"}),

        }

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)

    
    def clean(self):
        super(AddressForm, self).clean()
        name = self.cleaned_data.get("name")
        pincode = self.cleaned_data.get("pincode")
        phone = self.cleaned_data.get("phone")
       
        if len(name) < 5:
            self._errors['name'] = self.error_class(['Minimum 5 characters required'])

        if len(pincode) != 6:
            self._errors['pincode'] = self.error_class(['Pincode Should Contain an exact 6 Numbers'])

        if len(phone) != 10:
            self._errors['phone'] = self.error_class(['Mobile No. Should Contain an exact 10 Numbers'])
 
        return self.cleaned_data