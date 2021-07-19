from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _


# Create your models here.
class CustomOrder(models.Model):
    title = models.CharField(_("Title "), max_length=50)
    name = models.CharField(_("Name "), max_length=50)
    email = models.EmailField(_("Email"), max_length=254)
    phone = models.CharField(_("Phone"), max_length=70)
    address = models.CharField(_("Address"), max_length=70)
    
    
    class Meta:
        db_table = 'customer_orders'
        managed = True
        verbose_name = 'customer order'
        verbose_name_plural = 'customer orders'

class Segment(models.Model):
    title = models. CharField(_("Title"), max_length=50)
    category = models. CharField(_("Title"), max_length=50)

class Payment(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    objects = models.Manager()

    def __str__(self):
        return self.title

class Stock(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    objects = models.Manager()

    def __str__(self):
        return self.title
    

class Order(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    objects = models.Manager()

    def __str__(self):
        return self.title

class Discount(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    objects = models.Manager()

    def __str__(self):
        return self.title

class Taxes(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    objects = models.Manager()

    def __str__(self):
        return self.title

class Customer(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    objects = models.Manager()

    def __str__(self):
        return self.title

class Store(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    objects = models.Manager()

    def __str__(self):
        return self.title

class Product(models.Model):
    product_no = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(_("name of product"),max_length=100,help_text='', unique=True)
    brand_name = models.CharField(_("brand name"), null=True, blank=True, max_length=100)
    price = models.FloatField(_("Cost /Unit"),default=0)
    profit = models.FloatField(_("profit needed /Unit"),default=0,help_text='profit expected per Unit')
    created_at = models.DateField(_("Date of creation"),default=timezone.now)
    updated_at = models.DateField(_("Updated date"),default=timezone.now)
    # product_type = models.ForeignKey('ProductType', null=False, blank=True, on_delete=models.CASCADE)
    


    class Meta:
        db_table = "products"
        verbose_name = ("product")
        verbose_name_plural = "products"
        
    def __str__(self):
        return self.commercial_name or self.name 

    class Meta:
        ordering = ['product_no', ]
        db_table = 'products'
        # permissions = (('can_view_room', 'Can view room'),)

    def __str__(self):
        return "%s - %s - %i Rwf. " % (self.product_no, self.product_type.name, self.product_type.price)

    def display_feature(self):
        """
        This function should be defined since facility is many-to-many relationship
        It cannot be displayed directly on the admin panel for list_display
        """
        return ', '.join([feature.name for feature in self.features.all()])

    display_feature.short_description = 'Features'
    
    # def get_productfeatures(self):
    #     return self.features.all()
    
    @property
    def get_pictures(self):
        return self.product_pictures.all()
    
    @property
    def get_product_mark(self):
        return self.product_mark.all()

class ProductPicture(models.Model):
    product = models.ForeignKey(
        "Product", 
        verbose_name =_("product picture"), 
        related_name='product_pictures',
        on_delete=models.CASCADE
        )
    image = models.ImageField(
        max_length=255,
        upload_to="product_pictures/",
        )
    
    def __str__(self) -> str:
        return ""

    class Meta:
        db_table = 'product_pictures'
        managed = True
        verbose_name = 'ProductPicture'
        verbose_name_plural = 'ProductPictures'

# class ProductFeature(models.Model):
#     name = models.CharField(max_length=25)
#     price = models.PositiveSmallIntegerField()
    
#     def __str__(self):
#         return self.name

#     class Meta:
#         db_table = 'features'
#         managed = True
#         verbose_name = 'feature'
#         verbose_name_plural = 'Features'

class ProductMark(models.Model):
    name = models.CharField(max_length=25)
    price = models.PositiveSmallIntegerField()
    
    class Meta:
        db_table = 'product_mark'
        managed = True
        verbose_name = 'product mark'
        verbose_name_plural = 'product mark'

    def __str__(self):
        return "%s (%s) Frw"%(self.name, self.price)
