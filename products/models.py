from django.db import models
from base.models import BaseModel
from django.utils.text import slugify

# Create your models here.
class Publication(BaseModel):
    name = models.CharField(max_length=500)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Publication, self).save(*args, **kwargs)

    def __str__(self) : 
        return self.name
    


class Category(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='categories')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self) : 
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'



class SubCategory(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(SubCategory, self).save(*args, **kwargs)

    def __str__(self) : 
        return self.name
    
    class Meta:
        verbose_name_plural = 'SubCategories'



class Author(BaseModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Author, self).save(*args, **kwargs)

    def __str__(self) : 
        return self.name


class Product(BaseModel):
    secondery_uid = models.UUIDField(null = True, blank = True)
    title = models.CharField(max_length=1000)
    slug = models.SlugField(unique=True, null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author_products' , null=True, blank=True)
    isbn = models.CharField(max_length=13, null=True, blank=True)
    publication_year = models.IntegerField(null=True, blank=True)
    publication_id = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='publication_products')
    categories = models.ManyToManyField(Category, blank=True)
    subcategories = models.ManyToManyField(SubCategory, blank=True)
    image = models.ImageField(upload_to='products')

    weight = models.IntegerField(null=True, blank=True)
    language = models.CharField(max_length = 50, null=True, blank=True)

    prod_code_1 = models.CharField(null=True, blank=True)
    prod_code_2 = models.CharField(null=True, blank=True)

    # prices 
    mrp = models.IntegerField(null=True, blank=True)

    normal_price = models.IntegerField(null=True, blank=True)
    normal_discount_percenatage = models.IntegerField(null=True, blank=True)

    prime_price = models.IntegerField(null=True, blank=True)
    prime_discount_percenatage = models.IntegerField(null=True, blank=True)

    dealer_price = models.IntegerField(null=True, blank=True)
    dealer_discount_percenatage = models.IntegerField(null=True, blank=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)

    def __str__(self):
        return self.coupon_code
